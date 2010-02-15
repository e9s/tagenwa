# -*- coding: UTF-8 -*-
"""
Language identifier

"""
__version__ = "0.1"
__license__ = "MIT"

from hmm import AbstractHMM
from util import sliding_tuples

from math import log, log1p



def bigrams(text):
	"""Generate an iterable of bigrams from the text.
	
	:param text: a string
	:type text: unicode
	:return: iterable of bigrams
	:rtype: tuple generator
	"""
	return sliding_tuples(text, 2)


def trigrams(text):
	"""Generate an iterable of trigrams from the text.
	
	:param text: a string
	:type text: unicode
	:return: iterable of trigrams
	:rtype: tuple generator
	"""
	# skip tuples with two consecutive 'None'
	# without this, the tuples containing only the first or the last letter tuples
	# have too much weight as they appear more frequently
	return (tu for tu in sliding_tuples(text, 3) if tu[1] is not None)



def set_lang(tokens, lang):
	"""Set the language of the iterable of tokens.
	
	:param tokens: iterable of tokens
	:type tokens: iterable
	:param lang: language (ISO 639 language code)
	:type lang: unicode
	:return: iterable of tokens with the property "lang" set to `lang` 
	:rtype: iterable
	"""
	return (t.set(u'lang',lang) for t in tokens)



class NGramHMMLanguageIdentifier(AbstractHMM):
	"""Language identifier using a hidden markov model for
	the language identification of the sequence of tokens.  The probability
	of emission in the hidden markov model is calculated
	using a Bayesian estimate of the ngram probability.
	"""
	
	def __init__(self, n=3, ngram_generator=trigrams, nsymbols=26):
		"""Create a new language identifier.
		
		:param n: size of the ngram
		:type n: int
		:param ngram_generator: function returning an iterable of ngrams from a Token
		:type ngram_generator: function
		:param nsymbols: average number of symbols of the known languages
		:type nsymbols: int
		"""
		self.states = set([None])
		self.frequencies = {}
		self.frequency_totals = {}
		self.n = n
		self.prior_ngram = nsymbols**n
		self.logprob_uniform = n * -log(nsymbols)
		self.ngram_generator = ngram_generator
	
	
	def shouldguess(self, token):
		"""Return True if the token should be guessed, False otherwise."""
		return not token.isspace() or token.iseol()
	
	
	def guess(self, tokens, initarg=None):
		"""Guess the language of the tokens by adding a `lang` property
		to each non whitespace token.
		
		If the language cannot be guessed, the value `None` is set.
		
		:param tokens: iterable of Tokens
		:type tokens: iterable
		:param initarg: parameter sent to loginit for the calculation of the initial probabilities
		:return: iterable of Tokens with the `lang` property
		:rtype: iterable
		"""
		tokens = list(tokens)
		
		# filter tokens for which we are guessing the language
		guesstokens = (t for t in tokens if self.shouldguess(t))
		
		languages = super(NGramHMMLanguageIdentifier,self).viterbi(guesstokens, initarg)
		# tag tokens for which we guessed the language
		iterpath = iter(languages)
		return (t.set(u'lang', iterpath.next()) if self.shouldguess(t) else t for t in tokens)
	
	
	def train(self, tokens, lang):
		"""Train the emission probabilities by counting the ngram frequencies.
		"""
		# add language if not existing
		if lang not in self.frequencies:
			self.states.add(lang)
			self.frequencies[lang] = {}
			self.frequency_totals[lang] = 0
		
		# update the ngrams frequencies
		ngrams = self.ngram_generator
		freqs = self.frequencies[lang]
		total = 0
		for t in tokens:
			for tu in ngrams(t.text):
				total += 1
				freqs[tu] = freqs.get(tu, 0) + 1
		
		# update the total frequency
		self.frequency_totals[lang] += total
	
	
	def loginit(self, initarg):
		"""Return the initial log-probability of each language."""
		# all languages are equally probable
		return dict((lang,0.0) for lang in self.states)
	
	
	def logtrans(self, lang2, token1, token2):
		"""Return the transition log-probability from each language"""
		if token1.isterm():
			v_same, v_change = log1p(-1E-15), log(1E-15)
		elif not token1.isterm() and token2.isterm():
			v_same, v_change = log1p(-1E-9), log(1E-9)
		else:
			v_same, v_change = log1p(-1E-6), log(1E-6)
		return dict((lang1,v_change if lang1 != lang2 else v_same) for lang1 in self.states)
	
	
	def logemit(self, token):
		"""Return the emission log-probability of each language"""
		ngrams = list(self.ngram_generator(token.text))
		length = len(ngrams)
		
		if length == 0 or not token.isword():
			# if ngrams is empty all languages are equally probable
			scores = dict((lang, 0.0) for lang in self.states)
		else:
			scores = dict(
				(
					lang,
					self.score(ngrams,lang)
				) for lang in self.frequencies
			)
			# calculate the log-probability of to beat to be classified as a known language
			# log-probability of a imaginary uniformly distributed language
			scores[None] = length * self.logprob_uniform
		
		return scores
	
	
	def score(self, ngrams, lang):
		"""Return the emission log-probability using the posterior distribution of the ngrams."""
		# get language frequencies
		freqs = self.frequencies[lang]
		total_freq = self.frequency_totals[lang]
		
		# calculate logprob
		return sum(log1p(freqs.get(g,0.0)) for g in ngrams) - log(self.prior_ngram + total_freq) * len(ngrams)
	
