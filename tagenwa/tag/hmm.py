# -*- coding: UTF-8 -*-
"""
Abstract classes for a HMM tagger and a classifier-based HMM tagger
"""
from math import log

from nltk.tag.api import TaggerI, FeaturesetTaggerI



class AbstractHMMTaggerI(TaggerI):
	
	def tag(self, unlabeled_sequence):
		"""Tag the given sequence with the highest probable state sequence."""
		labels = self.viterbi(unlabeled_sequence)
		return zip(unlabeled_sequence, labels)
	
	def loginit(self):
		"""Return the initial log-probability of each state.
		
		:return: initial log-probability of each state
		:rtype: dict
		"""
		raise NotImplementedError()
	
	def logemit(self, featureset):
		"""Return the emission log-probability of each language
		
		:return: emission log-probability of each state
		:rtype: dict
		"""
		raise NotImplementedError()
	
	def logtrans(self, featureset1, featureset2):
		"""Return the transition log-probability of each pair of states
		
		:param element1: previous observable element
		:param element2: current observable element
		:return: transition log-probability of each pair of states
		:rtype: dict
		"""
		raise NotImplementedError()
	
	
	def viterbi(self, iterable):
		"""Return the most probable sequence of hidden states.
		
		:param iterable: iterable of observable elements to tag 
		:type iterable: iterable
		:return: sequence of tags
		:rtype: list
		"""
		
		# shortcuts
		logemit = self.logemit
		logtrans = self.logtrans
		states = self.states
		
		# set the log-probabilities of the first element
		p = self.loginit()
		P = dict((j, p[j]) for j in states)
		# initialize the matrix of best previous elements
		V = []
		# set the previous observable element to the first element
		iterator = iter(iterable)
		try:
			ti = iterator.next()
		except StopIteration:
			# empty iterator
			return []
		
		# search for the best path and the log-probability of the states sequence
		for tj in iterator:
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
	


class ClassifierBasedHMMTagger(AbstractHMMTaggerI, FeaturesetTaggerI):
	
	def __init__(self, classifier, loginit=None, logtrans=None, *args, **kwargs):
		"""Create a hidden Markov model tagger where the emission probability
		is calculated by a classifier.
		
		"""
		# Get the classifier and the list of possible states
		self._classifier = classifier
		self.states = self._classifier.labels()
		
		# Overload the initial and transition log-probability functions if given
		if loginit is not None:
			self.loginit = loginit	
		if logtrans is not None:
			self.logtrans = logtrans
		
		# Calculate the log value of the uniform probability over all the states
		self._uniform_logprob = log(1.0 / len(self.states))
	
	
	def classifier(self):
		"""Return the classifier."""
		return self._classifier
	
	
	def loginit(self):
		"""Return a default uniform initial probability."""
		return dict((s, self._uniform_logprob) for s in self.states)
	
	
	def logemit(self, featureset):
		"""Return the emission probability from the classifier."""
		emit = self._classifier.prob_classify(featureset)
		return dict((s, emit.logprob(s)) for s in emit.samples())
	
	
	def logtrans(self, featureset1, featureset2):
		"""Return a default uniform transition probability."""
		return dict(((s1, s2), self._uniform_logprob) for s1 in self.states for s2 in self.states)

