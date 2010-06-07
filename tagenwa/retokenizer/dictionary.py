# -*- coding: UTF-8 -*-
"""
Dictionary-based retokenizer

"""
from tagenwa.token import Token
from tagenwa.util import sub


class DictionaryRetokenizer(object):
	"""Dictionary-based retokenizer."""
	
	def __init__(self, key=None):
		self.dictionary = {}
		self._dictionary_key_maxlength = 0
		if key is not None:
			self._key = key
		else:
			self._key = lambda x:tuple(t.text if hasattr(t,'text') else t for t in x)
		self._match = lambda x:self._key(x) in self.dictionary
		self._replace = lambda x:list(Token(t) for t in self.dictionary[self._key(x)])
	
	def add(self, key, replacement):
		tuple_key = tuple(key)
		if tuple_key in self.dictionary:
			raise KeyError('Key %s already exists in the dictionary.' % repr(key))
		self.dictionary[tuple_key] = replacement
		
		# update the max length
		if len(tuple_key) > self._dictionary_key_maxlength:
			self._dictionary_key_maxlength = len(tuple_key)
	
	def key(self, data):
		return self._key(data)
	
	def value(self, key):
		return self.dictionary[key]

	def retokenize(self, tokens):
		return sub(
			tokens,
			self._match,
			self._replace,
			self._dictionary_key_maxlength
		)


class MonolingualDictionaryRetokenizer(DictionaryRetokenizer):
	"""Dictionary-based retokenizer that only accepts tokens from a specific language."""

	def __init__(self, lang, key=None):
		DictionaryRetokenizer.__init__(self, key)
		self._match = lambda x:self._key(x) in self.dictionary \
			and None not in x \
			and all(i.get(u'lang') == lang for i in x)
