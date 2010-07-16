# -*- coding: UTF-8 -*-
"""
Token combining a unicode text and a properties dictionary.

"""
__version__ = "0.1"
__license__ = "MIT"

from uniscript import script
from util import copycase
from copy import deepcopy
from unicodedata import category as ucategory


###########################################################
# Token class
###########################################################

class Token(object):
	"""Token combining a unicode text and a properties dictionary."""
	
###########################################################
# Constructors
###########################################################
	
	def __init__(self, text):
		"""Create a new Token."""
		if isinstance(text, unicode):
			self.text = text
			self.properties = {u'original':text}
		elif isinstance(text, Token):
			self.text = text.text
			self.properties = deepcopy(text.properties)
		else:
			raise TypeError('Only unicode and Token are supported, got %s.' % type(text).__name__)
	
	def copy(self, text=None):
		"""Create a new Token by copy (optionally with a new text)."""
		t = Token(self)
		if text is not None:
			t.text = text
		return t
	
###########################################################
# Properties manipulations
###########################################################

	def set(self, key, value):
		"""Set the property to the given value and return the token."""
		self.properties[key] = value
		return self
	
	def delete(self, key):
		"""Delete the property if it is defined and return the token."""
		if key in self.properties:
			del self.properties[key]
		return self
	
	def has(self, key):
		"""Check if the property is defined."""
		return key in self.properties
	
	def get(self, key, default=None):
		"""Return the property value if the property is defined, else 'default'.  If 'default' is not given, it defaults to 'None'."""
		return self.properties.get(key,default)
	
	
###########################################################
# Text manipulations
###########################################################

	def join(self, iterables):
		t = Token(self.text.join(iterables))
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
		t = Token(self)
		t.text = f(t.text, *args, **kwargs)
		return t
	
	def __getitem__(self, key):
		return self.text[key]
	def __getslice__(self, *slice):
		return self._copy_and_apply_to_text(unicode.__getslice__, *slice)
	
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
	
	def __iter__(self):
		return iter(self.text)

	def __contains__(self, string):
		return string in self.text
	def __eq__(self, y):
		if isinstance(y, Token):
			return self.text == y.text and self.properties == y.properties
		elif isinstance(y, unicode):
			return self.text == y
	def __len__(self):
		return len(self.text)
	def endswith(self, string):
		return self.text.endswith(string)
	def haslatin(self):
		return any(script(c, avoid_common=True) == 'Latin' for c in self.text)
	def isalnum(self):
		"""Return true if all characters in the token are alphanumeric and there is at least one character, false otherwise."""
		return self.text.isalnum()
	def isalpha(self):
		"""Return true if all characters in the token are alphabetic and there is at least one character, false otherwise."""
		return self.text.isalpha()
	def isdecimal(self):
		"""Return true if all characters in the token are decimal characters, false otherwise.
		
		Decimal characters include digit characters, and all characters that that can be used to form decimal-radix numbers, e.g. U+0660, ARABIC-INDIC DIGIT ZERO."""
		return self.text.isdecimal()
	def isdigit(self):
		"""Return true if all characters in the token are digits and there is at least one character, false otherwise."""
		return self.text.isdigit()
	def iseol(self):
		"""Return true if all characters in the token are end-of-line characters and there is at least one character, false otherwise."""
		return all(c in u'\n\r' for c in self.text)
	def ishexadecimal(self):
		"""Return true if the token is of the form 0x[0-9a-fA-F]+, false otherwise."""
		t = self.text
		return len(t) > 2 and t[:2] == u'0x' and all(c in u'0123456789abcdefABCDEF' for c in t[2:])
	def islower(self):
		"""Return true if all cased characters in the string are lowercase and there is at least one cased character, false otherwise."""
		return self.text.islower()
	def isnumeric(self):
		"""Return true if all characters in the token are numeric characters, false otherwise.
		
		Numeric characters include digit characters, and all characters that have the Unicode numeric value property, e.g. U+2155, VULGAR FRACTION ONE FIFTH."""
		return self.text.isnumeric()
	def isspace(self):
		"""Return true if all characters in the token are whitespace and there is at least one character, false otherwise."""
		return self.text.isspace()
	def isterm(self):
		"""Return true if any character in the token is a letter or a digit and there is at least one character, false otherwise."""
		return any(ucategory(c).startswith('L') or ucategory(c) == 'Nd' for c in self.text)
	def istitle(self):
		return self.text.istitle()
	def isupper(self):
		"""Return true if all cased characters in the string are uppercase and there is at least one cased character, false otherwise."""
		return self.text.isupper()
	def startswith(self, string):
		return self.text.startswith(string)
	def isword(self):
		"""Return true if the token is a word (only contains letters or dash punctuations), false otherwise."""
		return all(
			ucategory(c).startswith('L') or ucategory(c) == 'Pd' for c in self.text
		) and not all(
			ucategory(c) == 'Pd' for c in self.text
		)
	
###########################################################
# String conversions
###########################################################
	
	def __unicode__(self):
		return self.text
	
	def __repr__(self):
		return self.text.encode('unicode_escape')+'{'+', '.join(unicode(k).encode('unicode_escape')+':'+repr(v) for k,v in self.properties.iteritems())+'}'



###########################################################
# Useful functions to manipulate tokens
###########################################################

def set_property(tokens, name, value_function, *args, **kwargs):
	"""Set the `name` property of an iterable of tokens to the returned value of the `value_function` function.
	
	The value of the property is defined by a function call `value_function(token, *args, **kwargs)`.
	"""
	return (token.set(name, value_function(token, *args, **kwargs)) for token in tokens)



