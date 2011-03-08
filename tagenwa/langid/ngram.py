# -*- coding: UTF-8 -*-
"""
Character n-gram language classifier

"""
__license__ = "MIT"

from collections import defaultdict
from math import log, log1p, exp
import unicodedata
import itertools
import re

from nltk.classify.api import ClassifierI
from nltk.probability import FreqDist, ELEProbDist, DictionaryProbDist

from tagenwa.utils import sliding_tuples, merge_tagged
from tagenwa.tag.hmm import ClassifierBasedHMMTagger



###############################################################################
# N-gram
###############################################################################

def build_ngram_function(n):
	"""Return an function returning a list of character n-grams from a string
	for use in language identification.
	
	The returned function accepts a Unicode string as parameter
	and returns a list of n-grams as Unicode strings.
	N-grams where the middle character(s) are not in the token are filtered out
	to avoid over-representing characters in the beginning and the end of the word.
	When the n-gram is not completely contained in the token, a space is used
	as a place-holder character.
	
	>>> get_trigrams = build_ngram_function(3)
	>>> get_trigrams(u'Abc')
	[u' ab', u'abc', u'bc ']
	
	:param n: size of the n-grams
	:type n: int
	:return: function returning a list of n-grams
	:rtype: function(unicode)
	"""
	# Assert that n is a strictly positive integer
	assert(isinstance(n, int) and n > 0)
	
	# List items that must not be None to be a ngram
	if n <= 2:
		check_not_none = []
	else:
		check_not_none = [(n - 1) / 2] if n % 2 else [n / 2 -1, n / 2]
	
	def get_ngrams(token):
		if _SPACEPUNCT.match(token) is not None:
			# If space or punctuation, don't return any n-grams
			return []
		return [u''.join(tu) for tu in sliding_tuples(token.lower(), n, fill_value=u' ') if all(tu[i] != u' ' for i in check_not_none)]
	return get_ngrams



###############################################################################
# Feature set
###############################################################################

_SPACEPUNCT = re.compile(ur'(\s+|\W)', re.U)

def tokenize(text, normalization_form='NFC'):
	"""Tokenize the text on spaces and punctuations"""
	text = unicodedata.normalize(normalization_form, text)
	return [t for t in _SPACEPUNCT.split(text) if t]



###############################################################################
# N-gram language classifier
###############################################################################

class NgramLanguageTraining(object):
	
	def __init__(self, n=None, ngram_function=None, tokenize_function=None):
		"""Create a new training instance for a n-gram language classifier."""
		self._freqdists = {}
		
		# Define the n-gram function
		if ngram_function is not None:
			self._ngrams = ngram_function
		elif n is not None:
			self._ngrams = build_ngram_function(n)
		else:
			raise ValueError('Either the argument n or the argument ngram_function must be specified.')
		
		# Define the tokenize function
		self._tokenize = tokenize_function if tokenize_function is not None else tokenize
	
	
	def add(self, text, language):
		"""Add the given text to the training data"""
		# Create the frequency distribution if it doesn't exist yet
		if language not in self._freqdists:
			self._freqdists[language] = FreqDist()
		freqdist = self._freqdists[language]
		
		# Update the frequency distribution
		tokens = self._tokenize(text)
		for token in tokens:
			freqdist.update(self._ngrams(token))
	
	
	def add_corpus(self, corpus, language):
		"""Add the given corpus to the training data"""
		for fileid in corpus.fileids():
			self.add(corpus.raw(fileid), language)
	
	
	def get_freqdists(self):
		"""Return the frequency distributions learned from the training data"""
		return self._freqdists
	
	
	def get_probdists(self):
		"""Return the probability distributions learned from the training data"""
		return dict((lang, ELEProbDist(self._freqdists[lang])) for lang in self._freqdists)
	


class NgramLanguageClassifier(ClassifierI):
	"""A n-gram language classifier.
	
	"""
	
	def __init__(self, training, cutoff=None):
		"""
		:param training: the training data for the language classification.
		:type training: NgramLanguageTraining
		"""
		self._training = training
		self._probdists = training.get_probdists()
		self._languages = self._probdists.keys() + [u'und']
		self._cutoff = cutoff
	
	
	def labels(self):
		"""Return the list of category labels used by this classifier."""
		return self._languages
	
	
	def score_classify(self, featureset):
		"""Return a dict of scores (unnormalized probability estimates) for each language for the given featureset."""
		
		if u'ngrams' not in featureset:
			raise ValueError('The feature set does not contain a feature named "ngrams".')
		
		# Calculate the score of each language as the unnormalized join probability of each n-gram
		scores = {}
		for lang in self._probdists:
			probdist = self._probdists[lang]
			scores[lang] = exp(sum(probdist.logprob(ngram) for ngram in featureset[u'ngrams']))
		# Add a score for the "undetermined language"
		if self._cutoff:
			scores[u'und'] = pow(self._cutoff, len(featureset[u'ngrams']))
		else:
			scores[u'und'] = min(scores.values())
		return scores
	
	
	def prob_classify(self, featureset):
		"""Return a probability distribution over labels for the given featureset."""
		scores = self.score_classify(featureset)
		return DictionaryProbDist(scores, normalize=True)
	
	
	def classify(self, featureset):
		"""Return the most appropriate label for the given featureset."""
		return self.prob_classify(featureset).max()
	
	
	def get_token_featureset(self, token):
		"""Return a featureset corresponding to the given token"""
		return {
			u'text': token,
			u'ngrams': self._training._ngrams(token),
		}
	
	
	def prob_classify_text(self, text):
		"""Return a probability distribution over labels for the given text."""
		tokens = self._training._tokenize(text)
		ngrams = itertools.chain.from_iterable(
			self._training._ngrams(token) for token in tokens
		)
		featureset = {
			u'text': text,
			u'ngrams': list(ngrams),
		}
		return self.prob_classify(featureset)
	
	
	def classify_text(self, text):
		"""Return the most appropriate label for the given text."""
		return self.prob_classify_text(text).max()



###############################################################################
# N-gram language classifier
###############################################################################

class NgramHMMLanguageTagger(ClassifierBasedHMMTagger):
	
	def __init__(self, classifier, loginit=None, logtrans=None, *args, **kwargs):
		super(NgramHMMLanguageTagger, self).__init__(classifier, loginit=loginit, logtrans=logtrans, *args, **kwargs)
		
	
	def logtrans(self, featureset1, featureset2):
		if not featureset2[u'ngrams']:
			pdiff = 1E-15
			log_not_pdiff = log1p(pdiff * (len(self.states)-1))
			log_pdiff = log(pdiff)
			return dict(((s1, s2), log_not_pdiff if s1==s2 else log_pdiff) for s1 in self.states for s2 in self.states)
		elif not featureset1[u'ngrams']:
			pdiff = 1E-20
			log_not_pdiff = log1p(pdiff * (len(self.states)-1))
			log_pdiff = log(pdiff)
			return dict(((s1, s2), log_not_pdiff if s1==s2 else log_pdiff) for s1 in self.states for s2 in self.states)
		else:
			pdiff = 1E-10
			log_not_pdiff = log1p(pdiff * (len(self.states)-1))
			log_pdiff = log(pdiff)
			return dict(((s1, s2), log_not_pdiff if s1==s2 else log_pdiff) for s1 in self.states for s2 in self.states)
	
	
	def tag_text(self, text):
		"""Return a list of tagged tokens from the given text."""
		tokens = self._classifier._training._tokenize(text)
		get_featureset = self._classifier.get_token_featureset
		labeled_sequence = self.tag([get_featureset(token) for token in tokens])
		return [(token[u'text'], tag) for token, tag in labeled_sequence]
	
	
	def split_text(self, text):
		"""Split the given text into a list of tuples (text part, language)."""
		return list(merge_tagged(self.tag_text(text), lambda x:u''.join(x)))

