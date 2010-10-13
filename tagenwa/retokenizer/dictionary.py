# -*- coding: UTF-8 -*-
"""
Dictionary-based retokenizer

"""
from itertools import islice

from tagenwa.token import Token
from tagenwa.util.trie import Trie
from tagenwa.util.tools import sub


def _default_key(tokens):
	return tuple(t.text if hasattr(t,'text') else t for t in tokens)


class DictionaryRetokenizer(object):
	"""Dictionary-based retokenizer."""
	
	def __init__(self, key=None):
		self.trie = Trie()
		
		self._key = key if key is not None else _default_key
		self._match = lambda x:True
	
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

	def retokenize(self, tokens, callback=lambda x,y:x):
		i = 0
		tokens = list(tokens)
		length = len(tokens)
		keyed_tokens = self._key(tokens)
		find_prefix = self.trie.find_prefix
		
		while i < length:
			# Search the longuest key in the trie
			prefix = find_prefix(islice(keyed_tokens, i, None))
			prefix_length = len(prefix)
			if prefix_length and self._match(tokens[i:i+prefix_length]):
				# Key found in the trie
				for c in callback((Token(t) for t in self.trie.get(prefix)), tokens[i:i+prefix_length]):
					yield c
				i += len(prefix)
			else:
				# Key not found in the trie
				yield tokens[i]
				i += 1


class MonolingualDictionaryRetokenizer(DictionaryRetokenizer):
	"""Dictionary-based retokenizer that only accepts tokens from a specific language."""

	def __init__(self, lang, key=None):
		DictionaryRetokenizer.__init__(self, key)
		self._match = lambda tokens:all(t.get(u'lang') == lang for t in tokens)
