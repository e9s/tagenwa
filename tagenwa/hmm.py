# -*- coding: UTF-8 -*-
"""
Abstract Hidden Markov Model

"""
__version__ = "0.1"
__license__ = "MIT"


class AbstractHMM(object):
	"""Abstract Hidden Markov Model.
	
	This abstract HMM implementation provides hooks for the calculation of 
	the initial, emission and transition probabilities
	using methods to be overridden.  It is designed to be versatile over
	easy to use or fast to execute.
	
	To be used the following attributes/methods should be overridden:
	* self.states
	* self.loginit()
	* self.logemit()
	* self.logtrans()
	"""
	
	def __init__(self):
		self.states = set()
	
	
	def viterbi(self, iterable, initarg=None):
		"""Return the most probable sequence of hidden states.
		
		:param iterable: iterable of observable elements to tag 
		:type iterable: iterable
		:param initarg: initial argument sent to loginit() (default value is None)
		:return: sequence of tags
		:rtype: list
		"""
		
		# shortcuts
		loginit = self.loginit
		logemit = self.logemit
		logtrans = self.logtrans
		states = self.states
		
		# set up the initial path and the log-probabilities
		T = {}
		for j in states:
			T[j] = (loginit(j, initarg),[])
		
		# search for the best path and the log-probability of the states sequence
		for t in iterable:
			U = {}
			p = logemit(t)
			for j in states:
				# get the best path until state "j" (excluded) and its log-probability
				logprob,i = max( (T[i][0] + logtrans(i,j,t), i) for i in states)
				# save the new path until "j" (included) and its log-probability
				U[j] = (logprob + p[j], T[i][1] + [j])
			T = U
		
		# get the best path and its log-probability
		logprob, path = max(T[i] for i in states)
		
		# return the Viterbi path
		return path
	
	
	def loginit(self, lang, initarg):
		"""Return the initial log-probability of the language."""
		raise NotImplementedError()
	
	
	def logtrans(self, lang1, lang2, token1):
		"""Return the transition log-probability of each language"""
		raise NotImplementedError()
	
	
	def logemit(self, token):
		"""Return the emission log-probability of each language"""
		raise NotImplementedError()
