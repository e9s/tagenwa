# -*- coding: UTF-8 -*-
"""
Single word n-gram language identifier

"""
__version__ = "0.1"
__license__ = "MIT"

from collections import defaultdict
from math import log, log1p

from tagenwa.util import sliding_tuples


def ngrams(n, token):
	"""Return an iterator of n-grams
	
	N-grams where the middle item(s) are not in the text are filtered out
	to avoid over-representing characters in the beginning and the end
	of the word.
	
	:param n: size of the n-grams
	:type n: int
	:param token: token from which n-grams should be generated
	:type token: Token
	:return: iterable of n-grams
	:rtype: generator of tuples
	"""
	# Assert that n is a strictly positive integer
	assert(isinstance(n, int) and n > 0)
	
	# List items that must not be None to be a ngram
	if n <= 2:
		check_not_none = []
	else:
		check_not_none = [(n - 1) / 2] if n % 2 else [n / 2 -1, n / 2]
	
	# Return the generator of ngrams
	return (tu for tu in sliding_tuples(token.text, n) if all(tu[i] is not None for i in check_not_none))



class NgramLanguageIdentifier(object):
	"""Single word n-gram language identifier
	
	"""
	
	def __init__(self, n, ngram_generator=None, prior=0.0, smoothing_coefficient=0.0):
		"""Create a single word n-gram language identifier.
		
		:param n: size of the n-grams
		:type n: int
		"""
		self.n = n
		self.frequencies = {}
		self.frequency_totals = {}
		self.ngram_generator = ngram_generator if ngram_generator else lambda x: ngrams(n, x)
		self.prior = prior
		self.smoothing_coefficient = smoothing_coefficient
	
	def get_known_languages(self):
		return self.frequencies.keys()
	
	def ngrams(self, token):
		return self.ngram_generator(token)
	
	def train(self, lang, tokens):
		"""Train the language identifier on the tokens."""
		# Generate the ngram frequency
		frequency = defaultdict(int)
		for t in tokens:
			for ngram in self.ngram_generator(t.text):
				frequency[ngram] += 1
		# Train
		return self.train_frequency(lang, frequency)
	
	
	def train_frequency(self, lang, frequency):
		"""Train the language identifier on the n-gram frequency."""
		# Add language if not existing
		if lang not in self.frequencies:
			self.frequencies[lang] = {}
			self.frequency_totals[lang] = 0
		# Update the ngrams frequencies
		frequencies_lang = self.frequencies[lang]
		for ngram in frequency:
			frequencies_lang[ngram] = frequencies_lang.get(ngram, 0) + frequency[ngram]
		# Update the total frequency
		self.frequency_totals[lang] += sum(frequency.itervalues())
	
	
	def estimate(self, token):
		"""Estimate the log probability of each known language for the token."""
		ngrams = list(self.ngram_generator(token))
		estimates = ((lang, self._estimate(lang, ngrams)) for lang in self.frequencies)
		return dict((k,v) for k,v in estimates if v is not None)
	
	
	def _estimate(self, lang, ngrams):
		"""Estimate the log probability of the token matching the language."""
		# No estimate if no ngrams
		length = len(ngrams)
		if not length:
			return None
		# Get language frequencies
		frequencies_lang = self.frequencies[lang]
		frequency_totals_lang = self.frequency_totals[lang]
		# Precalculate prior
		alpha = self.smoothing_coefficient * self.prior
		beta = self.smoothing_coefficient
		# Calculate log probability
		return (
			sum(log1p(alpha + frequencies_lang.get(ngram, 0.0)) for ngram in ngrams)
			- log(beta + frequency_totals_lang) * length
		)

