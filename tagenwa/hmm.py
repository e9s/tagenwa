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
		
		:param iterable: iterable of observable elements to classify 
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
		
		# set the initial path and the log-probabilities of the first element
		p = loginit(initarg)
		T = dict((j, (p[j],[j])) for j in states)
		# set the previous observable element to the first element
		try:
			ti = iterable.next()
		except StopIteration:
			# empty iterable
			return []
		
		# search for the best path and the log-probability of the states sequence
		for tj in iterable:
			U = {}
			pe = logemit(tj)
			for j in states:
				# get the best path until state "j" (excluded) and its log-probability
				pt = logtrans(j,ti,tj)
				logprob,i = max( (T[i][0] + pt[i], i) for i in states)
				# save the new path until "j" (included) and its log-probability
				U[j] = (logprob + pe[j], T[i][1] + [j])
			T = U
			# copy previous state
			ti = tj
		
		# get the best path and its log-probability
		logprob, path = max(T[i] for i in states)
		
		# return the Viterbi path
		return path
	
	
	def loginit(self, initarg):
		"""Return the initial log-probability of each state.
		
		:param initarg: argument passed from self.viterbi()
		:return: initial log-probability of each state
		:rtype: dict
		"""
		raise NotImplementedError()
	
	
	def logtrans(self, state2, element1, element2):
		"""Return the transition log-probability from each previous state
		
		:param state2: current state
		:param element1: previous observable element
		:param element2: current observable element
		:return: transition log-probability from each previous state
		:rtype: dict
		"""
		raise NotImplementedError()
	
	
	def logemit(self, element):
		"""Return the emission log-probability of each language
		
		:return: emission log-probability of each state
		:rtype: dict
		"""
		raise NotImplementedError()
