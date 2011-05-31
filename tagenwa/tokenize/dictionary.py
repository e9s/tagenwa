# -*- coding: UTF-8 -*-
"""
Dictionary-based retokenizer

"""
from itertools import islice
from tagenwa.utils.trie import Trie


class DictionaryRetokenizer(object):
	"""Dictionary-based retokenizer.
	
	The dictionary-based retokenizer can be used to replace sequence of tokens
	by synonyms or remove sequence of tokens (for stop words).
	
	"""
	
	def __init__(self, key=None, allow_overlap=False):
		"""Create a new dictionary-based retokenizer.
		
		:param key: function that transforms a sequence of tokens into a new sequence
		            to be used as key of the dictionary
		:type key: callable
		:param allow_overlap: allow overlapping sequence of tokens to be matched
		                      from the dictionary if true.
		:type allow_overlap: bool
		"""
		self.trie = Trie()
		self._key = key if key is not None else lambda x:x
		self.allow_overlap = allow_overlap
	
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
		prefix_end = 0
		length = len(tokens)
		while i < length:
			# Search the longuest key in the trie
			prefix = find_prefix(islice(keyed_tokens, i, None))
			prefix_length = len(prefix)
			
			if prefix and prefix_end < i + prefix_length:
				# Key found in the trie
				# and not included in the previous key
				
				# Update the position of the end of the key
				prefix_end = i + prefix_length
				
				# Return the items through the callback
				for c in callback(tokens[i:prefix_end], self.trie.get(prefix)):
					yield c
				
				# If overlap is not allowed, move to the end of the key
				# If it is allowed, just move of one item
				if self.allow_overlap:
					i += 1
				else:
					i = prefix_end
			else:
				# Key not found in the trie
				
				if (not self.allow_overlap) or prefix_end <= i:
					# Token not included in the previous key, yield it
					# (always the case when allow_overlap is False)
					yield tokens[i]
				i += 1
