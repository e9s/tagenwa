# -*- coding: UTF-8 -*-
"""
Single word n-gram language identifier

"""
__version__ = "0.1"
__license__ = "MIT"

from collections import defaultdict
from math import log, log1p

from tagenwa.util import sliding_tuples


def ngram_generator_factory(n):
	"""Return an function returning a list of n-grams of a token.
	
	The returned function accepts a Token as parameter and returns a list of n-grams as Unicode strings.
	N-grams where the middle character(s) are not in the token are filtered out
	to avoid over-representing characters in the beginning and the end 	of the word.
	When the n-gram is not completely contained in the token, None is used as a place-holder character.
	
	>>> from tagenwa.token import Token
	>>> f = ngram_generator_factory(3)
	>>> f(Token(u'abc'))
	[(None, u'a', u'b'), (u'a', u'b', u'c'), (u'b', u'c', None)]
	
	:param n: size of the n-grams
	:type n: int
	:return: function returning a list of n-grams
	:rtype: function(Token)
	"""
	# Assert that n is a strictly positive integer
	assert(isinstance(n, int) and n > 0)
	
	# List items that must not be None to be a ngram
	if n <= 2:
		check_not_none = []
	else:
		check_not_none = [(n - 1) / 2] if n % 2 else [n / 2 -1, n / 2]
	
	def ngram_generator(token):
		return [tu for tu in sliding_tuples(token.text, n) if all(tu[i] is not None for i in check_not_none)]
	return ngram_generator



class NgramLanguageIdentifier(object):
	"""Single word n-gram language identifier
	
	"""
	
	def __init__(self, n, ngram_generator=None, prior=0.0, smoothing_coefficient=0.0):
		"""Create a single word n-gram language identifier.
		
		If `ngram_generator` is None, the n-gram generator function is created automatically
		using the `ngram_generator_factory` function with the parameter `n`.
		
		The parameters `prior` and `smoothing_coefficient` define the parameters of the
		`beta-distributed <http://en.wikipedia.org/wiki/Beta_distribution>`_
		`conjugate prior <http://en.wikipedia.org/wiki/Conjugate_prior>`_
		used in the estimation of the language probabilities.
		They are linked to the parameters alpha and beta of the prior's beta distribution with the following relations:
		
		* alpha = `prior` * `smoothing_coefficient`
		* beta = (1 - `prior`) * `smoothing_coefficient`
		
		with 0 <= `prior` <= 1 and 0 <= `smoothing_coefficient`.
		
		:param n: the size of the n-grams
		:type n: int
		:param ngram_generator: a function that accepts a Token and return a list of n-grams (default: None)
		:type ngram_generator: function(Token)
		:param prior: the a priori probability
		:type prior: float
		:param smoothing_coefficient: the number of observations of the a priori probability
		:type smoothing_coefficient: float
		"""
		self.n = n
		self.frequencies = {}
		self.frequency_totals = {}
		self.log_frequencies = {}
		self.ngram_generator = ngram_generator if ngram_generator else ngram_generator_factory(n)
		self.prior = prior
		self.smoothing_coefficient = smoothing_coefficient
	
	def get_known_languages(self):
		"""Return the languages on which the identifier has been trained.	
		
		:rtype: list
		"""
		return self.frequencies.keys()
	
	def ngrams(self, token):
		"""Return the n-grams of the token.
		
		:param token: the token for which the n-grams are generated
		:type token: tagenwa.token.Token
		:return: a list of n-grams as Unicode strings
		:rtype: list
		"""
		return self.ngram_generator(token)
	
	def train(self, lang, tokens, process_training=True):
		"""Train the language identifier on the tokens.
		
		This method calls `train_frequency` behind the scene.
		
		:param lang: the language
		:param tokens: iterable of tokens to train on
		:param process_training: specifies whether to build the cache at the end of the training
		:type process_training: bool
		:return: None
		"""
		# Generate the ngram frequency
		frequency = defaultdict(int)
		for t in tokens:
			for ngram in self.ngram_generator(t.text):
				frequency[ngram] += 1
		# Train
		return self.train_frequency(lang, frequency, process_training)
	
	
	def train_frequency(self, lang, frequency, process_training=True):
		"""Train the language identifier on the n-gram frequency.
		
		:param lang: the language
		:param frequency: dictionary of n-gram frequencies to train on
		:type frequency: dict
		:param process_training: specifies whether to build the cache at the end of the training
		:type process_training: bool
		:return: None
		"""
		# Invalidate the cache
		self.log_frequencies = {}
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
		# Update the cache
		if process_training:
			self.process_training()
	
	
	def estimate(self, token):
		"""Estimate the log probability of each known language for the token.
		
		This method calls `estimate_ngrams` with the results of the `ngrams` method as parameter.
		
		:param token: the token to estimate
		:type token: tagenwa.token.Token
		:return: dictionary of the log probability for each language
		:rtype: dict
		"""
		ngrams = self.ngram_generator(token)
		return self.estimate(ngrams)
	
	
	def estimate_ngrams(self, ngrams):
		"""Estimate the log probability of each known language for the list of n-grams.
		
		:param ngrams: the n-grams to estimate
		:type ngrams: list
		:return: dictionary of log probability for each language
		:rtype: dict
		"""
		if not ngrams:
			# All languages are equally probable
			return dict((lang, 0.0) for lang in self.frequencies)
		
		assert self.log_frequencies, 'Please first initialize the cache by running the build_cache() method'
		
		# Precalculate prior
		alpha = self.smoothing_coefficient * self.prior
		beta = self.smoothing_coefficient * (1.0 - self.prior)
		log1p_alpha = log1p(alpha)
		length = len(ngrams)
		
		estimates = {}
		for lang in self.frequencies:
			log_frequencies_lang_get = self.log_frequencies[lang].get
			estimates[lang] = (
				sum(log_frequencies_lang_get(ngram, log1p_alpha) for ngram in ngrams)
				- log(beta + self.frequency_totals[lang]) * length
			)
		return estimates
	

	def process_training(self):
		"""Process the training.
		
		A log frequency cache is needed when running the estimate() methods and
		needs to be built after the model has been trained.
		
		:return: None
		"""
		alpha = self.smoothing_coefficient * self.prior
		self.log_frequencies = {}
		for lang in self.frequencies:
			frequencies_lang = self.frequencies[lang]
			self.log_frequencies[lang] = dict(
				(ngram, log1p(alpha + frequencies_lang[ngram])) for ngram in frequencies_lang
			)
