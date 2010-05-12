# -*- coding: UTF-8 -*-
"""
Dictionary-based retokenizer

"""
from tagenwa.token import Token
from tagenwa.util import sub


class DictionaryRetokenizer(object):
	
	def __init__(self, key=None):
		self.dictionary = {}
		self._dictionary_key_maxlength = 0
		if key is not None:
			self._key = key
		else:
			self._key = lambda x:tuple(t.text if hasattr(t,'text') else t for t in x)
		self._match = lambda x:self._key(x) in self.dictionary
		self._replace = lambda x:list(self.dictionary[self._key(x)])
	
	def add(self, key, replacement):
		tuple_key = tuple(key)
		self.dictionary[tuple_key] = replacement
		
		# update the max length
		if len(tuple_key) > self._dictionary_key_maxlength:
			self._dictionary_key_maxlength = len(tuple_key)
	
	def retokenize(self, tokens):
		return sub(
			tokens,
			self._match,
			self._replace,
			self._dictionary_key_maxlength
		)

