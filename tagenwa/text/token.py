# -*- coding: UTF-8 -*-
from unicodedata import category as ucategory

def iseol(text):
	"""Return true if all characters in the text are end-of-line characters
	and there is at least one character, false otherwise.
	
	:rtype: bool
	"""
	return all(c in u'\n\r' for c in text) and len(text) > 0


def ishexadecimal(text):
	"""Return true if the text is of the form 0x[0-9a-fA-F]+, false otherwise.
	
	:rtype: bool
	"""
	return len(text) > 2 and text[:2] == u'0x' and all(c in u'0123456789abcdefABCDEF' for c in text[2:])


def isterm(text):
	"""Return true if any character in the text is a letter or a number
	and there is at least one character, false otherwise.
	
	:rtype: bool
	"""
	return any(ucategory(c)[0] in 'LN' for c in text)


def isword(text):
	"""Return true if the token is a word (only contains letters or dash punctuations), false otherwise.
	
	:rtype: bool
	"""
	return all(
		ucategory(c).startswith('L') or ucategory(c) == 'Pd' for c in text
	) and not all(
		ucategory(c) == 'Pd' for c in text
	)
