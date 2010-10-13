# -*- coding: UTF-8 -*-
"""
Hidden Markov language identifier using n-gram emission probablities.

"""
__version__ = "0.1"
__license__ = "MIT"

from math import log, log1p

from tagenwa.util.hmm import AbstractHMM


class NgramHMMLanguageIdentifier(AbstractHMM):
	"""Language identifier based on a hidden Markov model for the language identification
	of the sequence of tokens.  The probability of emission in the hidden markov model
	is calculated using a Bayesian estimate of the n-gram probability.
	"""
	
	def __init__(self, token_identifier, nsymbols=26):
		"""Create a new language identifier
		based on a `hidden Markov model <http://en.wikipedia.org/wiki/Hidden_Markov_model>`_
		with a Bayesian estimate of the n-gram probability as emission probability.
		
		:param token_identifier: the language identifier for individual tokens
		:type token_identifier: NgramLanguageIdentifier
		:param nsymbols: average number of symbols of the known languages
		:type nsymbols: int
		"""
		self.states = [None] + list(token_identifier.get_known_languages())
		self.token_identifier = token_identifier
		self.logprob_uniform = token_identifier.n * -log(nsymbols)
		self.logprob_zero = -9999.0
	
	
	def get_fixed_logemit(self, known_lang):
		"""Return the emission log-probability of each language for a token
		where one language is considered as known."""
		fixed_logemit = dict(
			(lang, self.logprob_zero) for lang in self.states
		)
		fixed_logemit[known_lang] = 0.0
		return fixed_logemit
	
	
	def should_guess(self, token):
		"""Return True if the language of the token should be guessed, False otherwise.
		
		Tokens for which the language should not be guessed are not taken into account
		during the language identification by the hidden Markov model.
		
		:param token: the token to be tested
		:type token: tagenwa.token.Token
		:rtype: bool
		"""
		return not token.isspace() or token.iseol()
	
	
	def guess(self, tokens, initarg=None):
		"""Guess the language of the tokens and add a `lang` property
		to each non whitespace token.
		
		If the language cannot be guessed, the value `None` is set.
		If the language is already defined, the existing value is preserved.
		
		:param tokens: iterable of Tokens
		:param initarg: parameter sent to loginit for the calculation of the initial probabilities
		:type initarg: dict
		:return: the iterable `tokens` with an additional `lang` property to each token for which the language should be guessed
		:rtype: iterator
		"""
		tokens = list(tokens)
		
		# filter tokens for which we are guessing the language
		guesstokens = (t for t in tokens if self.should_guess(t))
		
		languages = super(NgramHMMLanguageIdentifier, self).viterbi(guesstokens, initarg)
		# tag tokens for which we guessed the language
		iterpath = iter(languages)
		for t in tokens:
			if self.should_guess(t):
				lang = iterpath.next()
				if not t.has(u'lang'):
					yield t.set(u'lang', lang)
				else:
					yield t
			else:
				yield t
	
	
	def loginit(self, initarg=None):
		"""Return the initial log-probability of each language.
		
		If `initarg` is None, all languages are given an equal initial probability.
		If `initarg` is not None, then `initarg` is used as the initial dictionary of log-probability of each language.
		
		:param initarg: initial log-probabilities
		:type initarg: dict
		:rtype: dict
		"""
		if initarg is not None:
			return initarg
		# All languages are equally probable
		return dict((lang,0.0) for lang in self.states)
	
	
	def logtrans(self, token1, token2):
		"""Return the transition log-probability of each language pair for the given pair of tokens.
		
		:param token1: the first token in the transition for which the transition log-probabilities are calculated
		:type token1: tagenwa.token.Token
		:param token2: the second token in the transition for which the transition log-probabilities are calculated
		:type token2: tagenwa.token.Token
		:rtype: dict
		"""
		if token1.isterm():
			v_same, v_change = log1p(-1E-15), log(1E-15)
		elif not token1.isterm() and token2.isterm():
			v_same, v_change = log1p(-1E-9), log(1E-9)
		else:
			v_same, v_change = log1p(-1E-6), log(1E-6)
		return dict(((lang1,lang2), v_change if lang1 != lang2 else v_same) for lang1 in self.states for lang2 in self.states)
	
	
	def logemit(self, token):
		"""Return the emission log-probability of each language for the given token.
		
		:param token: the token for which the emission log-probabilities are calculated
		:type token: tagenwa.token.Token
		:rtype: dict
		"""
		
		if token.has(u'lang'):
			# If language is already known, fix it
			known_lang = token.get(u'lang') if token.get(u'lang') in self.states else None
			return self.get_fixed_logemit(known_lang)
		
		if not token.isword():
			# If tokens is not a word, all languages are equally probable
			scores = dict((lang, 0.0) for lang in self.states)
		else:
			ngrams = self.token_identifier.ngrams(token)
			scores = self.token_identifier.estimate_ngrams(ngrams)
			scores = dict(
				(lang, scores.get(lang, self.logprob_zero)) for lang in self.states
			)
			# Calculate the log-probability of to beat to be classified as a known language
			# Log-probability of a imaginary uniformly distributed language
			scores[None] = len(ngrams) * self.logprob_uniform
		
		return scores

