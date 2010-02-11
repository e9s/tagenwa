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
import re, unicodedata

# space and end-of-line regular expression patterns
_SPACE_PATTERN = re.compile(ur'(\s+)', re.U)
_EOL_PATTERN = re.compile(ur'([\n\r]+)', re.U)
_COLLAPSE_SPACE_PATTERN = re.compile(ur'^\s*$')


def tokenize(text):
	"""Tokenize a Unicode string into an iterable of tokens.
	
	Text is normalized into the normal form KC (form 'NFKC' in unicodedata.normalize)
	which applies the compatibility decomposition followed by the canonical composition.
	
	Text is stripped from leading and trailing white spaces.
	Consecutive space characters are converted into one ascii space (like in html) but
	end of lines are kept as in the original text.
	
	Writing scripts (e.g.: latin, cyrillic,...) are separated.
	
	Non-connecting punctuations and symbols are separated from alphanumeric characters.
	
	TODO: add doctest examples.
	
	>>> list(t.text for t in tokenize(u'Hello world!!'))
	[u'Hello', u' ', u'world', u'!!']
	
	:param text: text to be tokenized
	:type text: unicode
	:return: a generator of `Token`s
	:rtype: generator
	"""
	
	# strip the text and normalize the unicode characters
	text = u''.join(unicodedata.normalize('NFKC', c) for c in text.strip())
	
	# start tokenizing
	tokens = [text]
	# split by end-of-lines and spaces
	tokens = _resplit_by_pattern(tokens, _EOL_PATTERN)
	tokens = _resplit_by_pattern(tokens, _SPACE_PATTERN)
	# collapse spaces (but not end-of-lines) into a single ascii whitespace
	tokens = (t if '\n' in t or not _COLLAPSE_SPACE_PATTERN.match(t) else u' ' for t in tokens)
	
	# split by character scripts
	tokens = _resplit_by_class(tokens, _character_class)
	
	# split leading and trailing dashes
	tokens = _resplit_strip_dash(tokens)
	
	# return a generator of tokens
	return (Token(t) for t in tokens if t)


###########################################################
# Helper functions
###########################################################

def _resplit_by_pattern(tokens, pattern):
	"""Resplit the iterable of tokens using the regular expression pattern."""
	return (s for t in tokens for s in pattern.split(t) if s)


def _resplit_strip_dash(tokens):
	"""Resplit an iterable of tokens by splitting the leading and trailing dashes."""
	return (s for t in tokens for s in _split_strip_dash(t) if s)


def _split_strip_dash(text):
	"""Split leading and trailing dashes."""
	# shortcut when no split to do
	length = len(text)
	if length <= 1 or (text[0] != u'-' and text[-1] != u'-'):
		return (text,)
	
	# find leading dashes
	i = 0
	while i < length:
		if text[i] == u'-':
			i += 1
		else:
			break
	# find trailing dashes
	j = length - 1
	while j >= i:
		if text[j] == u'-':
			j -= 1
		else:
			break
	return (text[0:i], text[i:j+1], text[j+1:length])


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
		if buffer:
			# if not empty, yield the buffer then empty it
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
	cat = unicodedata.category(c)
	if cat in _UNICODE_CAT_MAPPING:
		return _UNICODE_CAT_MAPPING[cat]
	# splitting by script families
	else:
		s = script(c, avoid_common=True)
		if s:
			return s
		else:
			return 'Other'

