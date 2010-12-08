# -*- coding: UTF-8 -*-
"""
Multilingual preliminary tokenization for language identification.

Tokenization is done on spaces, end of lines, non-connecting punctuations,
symbols and changes of writing scripts.
"""

__version__ = "0.1"
__license__ = "MIT"


from uniscript import script
from token import Token
from unicodedata import normalize as unicodedata_normalize, category as unicodedata_category
import re

# space and end-of-line regular expression patterns
_EOL_PATTERN = re.compile(ur'([\n\r]+)', re.U)
_SPACE_PATTERN = re.compile(ur'(\s+)', re.U)
_COLLAPSE_SPACE_PATTERN = re.compile(ur'^\s*$', re.U)

_WORD_BOUNDARY_PATTERN = re.compile(ur'(\s+|\W)', re.U)

# TODO: http://www.unicode.org/reports/tr29/#Word_Boundaries

def tokenize(text, normalization_form='NFC'):
	"""Tokenize a Unicode string into an iterable of tokens.
	
	By default, the text is normalized into the normal form C (also known as the "NFC" normalization form)
	which applies the canonical decomposition followed by the canonical composition.
	This follows the `W3C recommendation <http://www.w3.org/TR/charmod-norm/#sec-ChoiceNFC>`_
	in the document `Character Model for the World Wide Web 1.0: Normalization <http://www.w3.org/TR/charmod-norm/>`_.
	The normalization form "NFKC" can be applied instead using the parameter `normalization_form`
	(see `unicodedata.normalize <http://docs.python.org/library/unicodedata.html#unicodedata.normalize>`_ for details).
	Normalization forms "NFD" and NFKD" are not allowed
	as the `re` module does not support them.
	
	Consecutive whitespace characters are converted into one ascii space (like in html).
	Consecutive end of line characters are kept but are combined as one token.
	
	Character from different writing scripts (e.g.: latin, cyrillic,...) are splitted
	into different tokens.  If a character is common to several script,
	it is considered to be belonging to the same script as the previous character.
	
	Non-connecting punctuations and symbols are separated from alphanumeric characters.
	
	>>> list(t.text for t in tokenize(u'Hello world!!'))
	[u'Hello', u' ', u'world', u'!', u'!']
	
	:param text: text to be tokenized
	:type text: unicode
	:return: a generator of `Token`s
	:rtype: generator
	"""
	
	# assert the normalization form is either NFC or NFKC
	assert normalization_form in ('NFC', 'NFKC'), 'Parameter normalization_form must be "NFC" or "NFKC"'
	
	# normalize the unicode characters and start tokenizing
	tokens = [unicodedata_normalize(normalization_form, text)]
	# split by end-of-lines and spaces
	tokens = _resplit_by_pattern(tokens, _EOL_PATTERN)
	tokens = _resplit_by_pattern(tokens, _SPACE_PATTERN)
	# collapse spaces (but not end-of-lines) into a single ascii whitespace
	tokens = (t if u'\n' in t or not _COLLAPSE_SPACE_PATTERN.match(t) else u' ' for t in tokens)
	
	# split by character scripts (TODO: this split on hyphen)
	tokens = _resplit_by_pattern(tokens, _WORD_BOUNDARY_PATTERN)
	
	# split by character scripts
	#tokens = _resplit_by_class(tokens, _character_class)
	tokens = _resplit_tokens(tokens, _split_script)
	
	# return a generator of tokens
	return (Token(t) for t in tokens if t)


###########################################################
# Helper functions
###########################################################

def _resplit_by_pattern(tokens, pattern):
	"""Resplit the iterable of tokens using the regular expression pattern."""
	return (s for t in tokens for s in pattern.split(t) if s)


def _resplit_tokens(tokens, split_function):
	"""Resplit an iterable of tokens using a token splitting function."""
	return (s for t in tokens for s in split_function(t) if s)


SAME_PREVIOUS_SCRIPTS = [u'Common', u'Inherited']
def _split_script(text):
	"""Split if the scripts of two consecutive characters are different.
	
	Common characters to several scripts and inherited characters
	are considered to be written in the same script as the previous character.
	"""
	current_script = None
	i = 0
	for j in xrange(len(text)):
		s = script(text[j])
		if s != current_script and s not in SAME_PREVIOUS_SCRIPTS and current_script is not None:
			yield text[i:j]
			i = j
		if s not in SAME_PREVIOUS_SCRIPTS:
			current_script = s
	yield text[i:]


def _resplit_by_class(tokens, get_class):
	"""Resplit the iterable of tokens so that all characters from each token is in the same character class.
	
	:param tokens: iterable of tokens
	:param get_class: - function returning the class of a single character
	"""
	buffer = []
	for t in tokens:
		# no split if only 1 character
		if len(t) == 1:
			yield t
			continue
		previous_class = None
		# iterate over characters
		for c in t:
			current_class = get_class(c)
			if current_class == previous_class or previous_class is None:
				# same category, just put the character in the buffer
				buffer.append(c)
			else:
				# different category, yield the buffer
				yield u''.join(buffer)
				buffer = [c]
			previous_class = current_class
		# end of the token
		yield u''.join(buffer)
		buffer = []
	return


# documentation about Unicode category:
# http://www.fileformat.info/info/unicode/category/index.htm
_UNICODE_CAT_MAPPING = {
# splitting punctuations (but not dashes and connectors)
	'Ps':u'P(', # punct open
	'Pi':u'P(', # punct open
	'Pe':u'P)', # punct close
	'Pf':u'P)', # punct close
	'Po':u'Po', # punct other
# splitting symbols (but not modifiers)
	'Sc':u'Sc', # currency
	'Sm':u'Sm', # math
	'So':u'So', # symbol other
}

def _character_class(c):
	"""Return the class of the character as used in the tokenization.
	
	:param c: a single unicode character
	:type c: unicode
	:return: character class as used in the tokenization
	:rtype: unicode
	"""
	
	# splitting by unicode category (punctuation and symbols)
	cat = unicodedata_category(c)
	if cat in _UNICODE_CAT_MAPPING:
		return c
	# splitting by script families
	else:
		s = script(c, avoid_common=True)
		if s:
			return s
		else:
			return u'Other'

