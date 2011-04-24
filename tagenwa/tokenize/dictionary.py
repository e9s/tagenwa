# -*- coding: UTF-8 -*-
"""
Dictionary-based retokenizer

"""
from itertools import islice
from tagenwa.utils.trie import Trie


class DictionaryRetokenizer(object):
	"""Dictionary-based retokenizer."""
	
	def __init__(self, key=None):
		self.trie = Trie()
		self._key = key if key is not None else lambda x:x
	
	def add(self, key, replacement):
		"""Add a new entry in the dictionary."""
		tuple_key = tuple(key)
		if tuple_key in self.trie:
			raise KeyError('Key %s already exists in the dictionary.' % repr(key))
		self.trie.add(tuple_key, replacement)
	
	def key(self, data):
		"""Return the normalized key."""
		return self._key(data)
	
	def __contains__(self, key):
		"""Return True if the key is already in the dictionary."""
		return tuple(key) in self.trie
	
	def __len__(self):
		"""Return the number of keys in the dictionary."""
		return len(self.trie)
	
	def value(self, key):
		"""Return the value for the specified key"""
		return self.trie.get(key)
	
	def retokenize(self, tokens, callback=lambda x,y:y):
		"""Retokenize the iterable of tokens using the dictionary.
		
		:param callback: callable that accepts a list of original tokens
		                 and its corresponding value in the dictionary
		                 and returns an iterable of tokens replacing it.
		                 By default, its value is `lambda x,y: y`.
		:type callback: callable
		"""
		if not isinstance(tokens, list):
			tokens = list(tokens)
		keyed_tokens = self._key(tokens)
		find_prefix = self.trie.find_prefix
		
		i = 0
		length = len(tokens)
		while i < length:
			# Search the longuest key in the trie
			prefix = find_prefix(islice(keyed_tokens, i, None))
			if prefix:
				# Key found in the trie: return the normalized result
				prefix_length = len(prefix)
				for c in callback(tokens[i:i+prefix_length], self.trie.get(prefix)):
					yield c
				i += prefix_length
			else:
				# Key not found in the trie: just return the token
				yield tokens[i]
				i += 1
