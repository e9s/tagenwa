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
		
		# set the log-probabilities of the first element
		p = loginit(initarg)
		P = dict((j, p[j]) for j in states)
		# initialize the matrix of best previous elements
		V = []
		# set the previous observable element to the first element
		try:
			ti = iterable.next()
		except StopIteration:
			# empty iterable
			return []
		
		# search for the best path and the log-probability of the states sequence
		for tj in iterable:
			Q = {}
			W = {}
			pe = logemit(tj)
			pt = logtrans(ti,tj)
			for j in states:
				# save the best previous element until state "j" (excluded) and its log-probability
				logprob, W[j] = max( (P[i] + pt[i,j], i) for i in states)
				# save the log-probability until "j" (included)
				Q[j] = logprob + pe[j]
			# update the log-probability and save the list of best previous elements
			P = Q
			V.append(W)
			# copy previous state
			ti = tj
		
		# reconstruct the Viterbi path from the matrix of previous elements
		logprob, j = max((P[i],i) for i in states)
		path = [j]
		for t in xrange(len(V)-1,-1,-1):
			j = V[t][j]
			path.append(j)
		path.reverse()
		
		# return the Viterbi path
		return path
	
	
	def loginit(self, initarg):
		"""Return the initial log-probability of each state.
		
		:param initarg: argument passed from self.viterbi()
		:return: initial log-probability of each state
		:rtype: dict
		"""
		raise NotImplementedError()
	
	
	def logtrans(self, element1, element2):
		"""Return the transition log-probability of each state pair
		
		:param element1: previous observable element
		:param element2: current observable element
		:return: transition log-probability of each state pair
		:rtype: dict
		"""
		raise NotImplementedError()
	
	
	def logemit(self, element):
		"""Return the emission log-probability of each language
		
		:return: emission log-probability of each state
		:rtype: dict
		"""
		raise NotImplementedError()
