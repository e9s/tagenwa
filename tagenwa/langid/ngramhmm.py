# -*- coding: UTF-8 -*-
"""
Hidden Markov language identifier using n-gram emission probablities.

"""
__version__ = "0.1"
__license__ = "MIT"

from math import log, log1p

from tagenwa.hmm import AbstractHMM


class NgramHMMLanguageIdentifier(AbstractHMM):
	"""Language identifier using a hidden markov model for
	the language identification of the sequence of tokens.  The probability
	of emission in the hidden markov model is calculated
	using a Bayesian estimate of the ngram probability.
	"""
	
	def __init__(self, token_identifier, nsymbols=26):
		"""Create a new language identifier.
		
		:param nsymbols: average number of symbols of the known languages
		:type nsymbols: int
		"""
		self.states = [None] + list(token_identifier.get_known_languages())
		self.token_identifier = token_identifier
		self.logprob_uniform = token_identifier.n * -log(nsymbols)
		self.logprob_zero = -9999.0
	
	
	def shouldguess(self, token):
		"""Return True if the token should be guessed, False otherwise."""
		return not token.isspace() or token.iseol()
	
	
	def guess(self, tokens, initarg=None):
		"""Guess the language of the tokens by adding a `lang` property
		to each non whitespace token.
		
		If the language cannot be guessed, the value `None` is set.
		If the language is already defined, the value is kept unless highly improbable.
		
		:param tokens: iterable of Tokens
		:type tokens: iterable
		:param initarg: parameter sent to loginit for the calculation of the initial probabilities
		:return: iterable of Tokens with the `lang` property
		:rtype: iterable
		"""
		tokens = list(tokens)
		
		# filter tokens for which we are guessing the language
		guesstokens = (t for t in tokens if self.shouldguess(t))
		
		languages = super(NgramHMMLanguageIdentifier, self).viterbi(guesstokens, initarg)
		# tag tokens for which we guessed the language
		iterpath = iter(languages)
		for t in tokens:
			if self.shouldguess(t):
				lang = iterpath.next()
				if not t.has(u'lang'):
					yield t.set(u'lang', lang)
				else:
					yield t
			else:
				yield t
	
	
	def loginit(self, initarg):
		"""Return the initial log-probability of each language."""
		if initarg:
			return initarg
		# All languages are equally probable
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
		
		length = len(list(self.token_identifier.ngrams(token)))
		
		if token.has(u'lang'):
			# If language is already known, fix it
			known_lang = token.get(u'lang') if token.get(u'lang') in self.states else None
			scores = dict(
				(lang, self.logprob_zero) for lang in self.states
			)
			scores[known_lang] = 0.0
		elif not token.isword():
			# If tokens is not a word, all languages are equally probable
			scores = dict((lang, 0.0) for lang in self.states)
		elif not length:
			# If tokens has no n-grams, all languages are equally probable
			scores = dict((lang, 0.0) for lang in self.states)
		else:
			scores = self.token_identifier.estimate(token)
			scores = dict(
				(lang, scores.get(lang, self.logprob_zero)) for lang in self.states
			)
			# Calculate the log-probability of to beat to be classified as a known language
			# Log-probability of a imaginary uniformly distributed language
			scores[None] = length * self.logprob_uniform
		
		return scores

