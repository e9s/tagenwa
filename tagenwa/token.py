# -*- coding: UTF-8 -*-
"""
Token combining a unicode text and a properties dictionary.

"""
__version__ = "0.1"
__license__ = "MIT"

import functools
from copy import deepcopy
from unicodedata import category as ucategory

from tagenwa.uniscript import script
from tagenwa.util.tools import copycase


###########################################################
# Token class
###########################################################

class Token(object):
	"""Token combining a unicode text and a properties dictionary."""
	
###########################################################
# Constructors
###########################################################
	
	def __init__(self, text, properties=None):
		"""Create a new Token.
		
		The `text` parameter must be a unicode string or a Token instance.
		If a Token instance is given, the text and the properties of the given token
		is copied when creating the new token.
		
		The optional `properties` parameter can be a `dict` or an iterable of key-value pairs and
		is used to update the properties of the new token.
		
		:param text: text of the new Token or a Token to copy from
		:type text: unicode or Token
		:param properties: properties to add to the new Token
		"""
		if isinstance(text, unicode):
			self._text = text
			self._text_properties_cache = {}
			self.properties = {u'original':text}
			if properties is not None:
				self.properties.update(properties)
		elif isinstance(text, Token):
			self._text = text.text
			# The _text_properties_cache is append-only so it can be shared safely
			self._text_properties_cache = text._text_properties_cache
			self.properties = deepcopy(text.properties)
			if properties is not None:
				self.properties.update(properties)
		else:
			raise TypeError("Parameter must be unicode or Token, got %s." % type(text).__name__)
	
	def copy(self, text=None, properties=None):
		"""Create a new Token by copy.
		
		:param text: text of the new Token
		:type text: unicode
		:param properties: properties to add to the new Token
		"""
		t = Token(self, properties)
		if text is not None:
			t.set_text(text)
		return t
	
###########################################################
# Text getter and setter
###########################################################
	
	def get_text(self):
		"""Return the token's text.
		
		:return: text of the token
		:rtype: unicode
		"""
		return self._text

	def set_text(self, text):
		"""Set the token's text.
		
		:param text: text of the token
		:type text: unicode
		:return: self
		:rtype: Token
		"""
		if not isinstance(text, unicode):
			raise TypeError("Text must be unicode, got %s." % type(text).__name__)
		self._text = text
		# Invalidate the cache
		self._text_properties_cache = {}
		return self
	
	text = property(get_text, set_text)
	
	def _text_property_caching(f):
		@functools.wraps(f)
		def _text_property_wrapper(self):
			if f.__name__ in self._text_properties_cache:
				return self._text_properties_cache[f.__name__]
			value = f(self)
			self._text_properties_cache[f.__name__] = value
			return value
		return _text_property_wrapper
	
###########################################################
# Properties getter and setter
###########################################################

	def set(self, key, value):
		"""Set the property to the given value and return the token.
		
		The `set` method returns the token itself to allows to chain several `set` method calls together.
		
		>>> Token(u'snake').set(u'lang', u'en').set(u'part-of-speech', u'noun')
		Token(u'snake', {u'lang': u'en', u'part-of-speech': u'noun', u'original': u'snake'})
		
		:param key: property key
		:type key: hashable
		:param value: property value
		:return: self
		:rtype: Token
		"""
		self.properties[key] = value
		return self

	def update(self, properties):
		"""Update the properties of the token and return it.
		
		:param properties: properties to add
		:type properties: dict
		:return: self
		:rtype: Token
		"""
		self.properties.update(properties)
		return self
	
	def delete(self, key):
		"""Delete the property if it is defined and return the token.
		
		:param key: property key
		:type key: hashable
		:return: self
		:rtype: Token
		"""
		if key in self.properties:
			del self.properties[key]
		return self
	
	def has(self, key):
		"""Check if the property is defined.
		
		:param key: property key
		:type key: hashable
		:return: True if the property is defined, False otherwise
		:rtype: bool
		"""
		return key in self.properties
	
	def get(self, key, default=None):
		"""Return the property value if the property is defined, else 'default'.
		If 'default' is not given, it defaults to 'None'.
		
		:param key: property key
		:type key: hashable
		:param default: default value
		:return: property value
		"""
		return self.properties.get(key,default)
	
	
###########################################################
# Text manipulations
###########################################################

	def join(self, iterables):
		t = Token(self._text.join(iterables))
		t.properties = copy(self.properties)
		# join original texts if Tokens
		t.properties[u'original'] = self.properties[u'original'].join(
			t.properties[u'original'] if isinstance(t, Token) else unicode(t)
			for t in iterables
		)
		return t
	#
	#def split(self, sep=None, maxsplit=None):
	#	texts = self.text.split(sep, maxsplit) if maxsplit is not None else self.text.split(sep)
	#	tokens = [Token(self) for t in texts]
	#	for to,te in zip(tokens,texts):
	#		to.text = te
	#	return tokens
	
	def _copy_and_apply_to_text(self, f, *args, **kwargs):
		return self.copy(f(self._text, *args, **kwargs))
	
	def __add__(self, y):
		return self._copy_and_apply_to_text(unicode.__add__, y)
	def copycase(self, reference):
		return self._copy_and_apply_to_text(copycase)
	def lower(self):
		return self._copy_and_apply_to_text(unicode.lower)
	def lstrip(self, chars):
		return self._copy_and_apply_to_text(unicode.lstrip, chars)
	def strip(self, chars):
		return self._copy_and_apply_to_text(unicode.strip, chars)
	def rstrip(self, chars):
		return self._copy_and_apply_to_text(unicode.rstrip, chars)
	def swapcase(self):
		return self._copy_and_apply_to_text(unicode.swapcase)
	def title(self):
		return self._copy_and_apply_to_text(unicode.title)
	def upper(self):
		return self._copy_and_apply_to_text(unicode.upper)
		
###########################################################
# Text slicing
###########################################################
	
	def __getitem__(self, key):
		return self._text[key]
	def __getslice__(self, *slice):
		return self._copy_and_apply_to_text(unicode.__getslice__, *slice)
	def __iter__(self):
		return iter(self._text)

	def __eq__(self, y):
		if isinstance(y, Token):
			return self._text == y.text and self.properties == y.properties
		elif isinstance(y, unicode):
			return self._text == y
	
###########################################################
# Text properties
###########################################################

	def __contains__(self, string):
		"""Return true if the token contains the specified string, false otherwise.
		
		:rtype: bool
		"""
		return string in self._text
	
	def __len__(self):
		"""Return the length of the token.
		
		:rtype: int
		"""
		return len(self._text)
	
	def endswith(self, string):
		"""Return true if the token ends with the specified string, false otherwise.
		
		:rtype: bool
		"""
		return self._text.endswith(string)
	
	def isalnum(self):
		"""Return true if all characters in the token are alphanumeric
		and there is at least one character, false otherwise.
		
		:rtype: bool
		"""
		return self._text.isalnum()
	
	def isalpha(self):
		"""Return true if all characters in the token are alphabetic
		and there is at least one character, false otherwise.
		
		:rtype: bool
		"""
		return self._text.isalpha()
	
	def isdecimal(self):
		"""Return true if all characters in the token are decimal characters, false otherwise.
		
		Decimal characters include digit characters,
		and all characters that that can be used to form decimal-radix numbers,
		e.g. U+0660, ARABIC-INDIC DIGIT ZERO.
		
		>>> Token(u'123').isdecimal()
		True
		>>> Token(u'①').isdecimal()
		False
		>>> Token(u'ⅱ').isdecimal()
		False
		
		:rtype: bool
		"""
		return self._text.isdecimal()
	
	def isdigit(self):
		u"""Return true if all characters in the token are digits
		and there is at least one character, false otherwise.
		
		>>> Token(u'123').isdigit()
		True
		>>> Token(u'①').isdigit()
		True
		>>> Token(u'ⅱ').isdigit()
		False
		
		:rtype: bool
		"""
		return self._text.isdigit()
	
	def islower(self):
		"""Return true if all cased characters in the string are lowercase
		and there is at least one cased character, false otherwise.
		
		:rtype: bool
		"""
		return self._text.islower()
	
	def isnumeric(self):
		u"""Return true if all characters in the token are numeric characters, false otherwise.
		
		Numeric characters include digit characters,
		and all characters that have the Unicode numeric value property,
		e.g. U+2155, VULGAR FRACTION ONE FIFTH.
		
		>>> Token(u'123').isnumeric()
		True
		>>> Token(u'①').isnumeric()
		True
		>>> Token(u'ⅱ').isnumeric()
		True
		
		:rtype: bool
		"""
		return self._text.isnumeric()
	
	def isspace(self):
		"""Return true if all characters in the token are whitespace
		and there is at least one character, false otherwise.
		
		:rtype: bool
		"""
		return self._text.isspace()
	
	def istitle(self):
		"""
		
		:rtype: bool
		"""
		return self._text.istitle()
	
	def isupper(self):
		"""Return true if all cased characters in the string are uppercase
		and there is at least one cased character, false otherwise.
		
		:rtype: bool
		"""
		return self._text.isupper()
	
	def startswith(self, string):
		"""Return true if the token starts with the specified string, false otherwise.
		
		:rtype: bool
		"""
		return self._text.startswith(string)
	
	@_text_property_caching
	def haslatin(self):
		"""Return true if the token contains at least one latin character, false otherwise.
		
		:rtype: bool
		"""
		return any(script(c, avoid_common=True) == 'Latin' for c in self._text)
	
	@_text_property_caching
	def iseol(self):
		"""Return true if all characters in the token are end-of-line characters
		and there is at least one character, false otherwise.
		
		:rtype: bool
		"""
		return all(c in u'\n\r' for c in self._text)
	
	@_text_property_caching
	def ishexadecimal(self):
		"""Return true if the token is of the form 0x[0-9a-fA-F]+, false otherwise.
		
		:rtype: bool
		"""
		t = self._text
		return len(t) > 2 and t[:2] == u'0x' and all(c in u'0123456789abcdefABCDEF' for c in t[2:])
	
	@_text_property_caching
	def isterm(self):
		"""Return true if any character in the token is a letter or a digit
		and there is at least one character, false otherwise.
		
		:rtype: bool
		"""
		return any(ucategory(c).startswith('L') or ucategory(c) == 'Nd' for c in self._text)
	
	@_text_property_caching
	def isword(self):
		"""Return true if the token is a word (only contains letters or dash punctuations), false otherwise.
		
		:rtype: bool
		"""
		return all(
			ucategory(c).startswith('L') or ucategory(c) == 'Pd' for c in self._text
		) and not all(
			ucategory(c) == 'Pd' for c in self._text
		)
	
###########################################################
# String conversions
###########################################################
	
	def __unicode__(self):
		"""Return the text of the token.
		
		:return: text of the token
		:rtype: unicode
		"""
		return self.text
	
	def __repr__(self):
		"""Return a representation of the token instance.
		
		:rtype: str
		"""
		return (
			'Token(' +
			repr(self.text) +
			', {' +
			', '.join(repr(k)+': '+repr(v) for k,v in self.properties.iteritems()) +
			'})'
		)



###########################################################
# Useful functions to manipulate tokens
###########################################################

def set_property(tokens, key, value_function, *args, **kwargs):
	"""Set the property `key` of all tokens to the value of the `value_function` function.
	
	The value of the property is defined by a function call `value_function(token, *args, **kwargs)`.
	
	:param tokens: iterable of tokens
	:param key: key of the property to be set
	:param value_function: callback function
	:type value_function: function
	:return: iterable of tokens
	:rtype: iterator
	"""
	return (token.set(key, value_function(token, *args, **kwargs)) for token in tokens)



