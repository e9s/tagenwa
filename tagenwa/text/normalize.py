# -*- coding: UTF-8 -*-
"""Useful functions for character normalization

See also
  http://en.wikipedia.org/wiki/Alphabets_derived_from_the_Latin
"""
import unicodedata
import re


################################################################################

def remove_combining_marks(text):
	"""Remove all combining marks from the text.
	
	The string characters are decomposed using the Unicode's NFD normalization
	and all the combining marks are removed.
	"""
	return u''.join(
		c for c in unicodedata.normalize('NFD', text)
		if not unicodedata.combining(c)
	)

################################################################################

_LIGATURE_TRANSLATIONS = {
	#ord(u'ß'): u'ss' or u'sz',
	ord(u'æ'): u'ae',
	ord(u'Æ'): u'AE',
	ord(u'œ'): u'oe',
	ord(u'Œ'): u'OE',
	ord(u'ĳ'): u'ij', # normalized away with NFKC
	ord(u'Ĳ'): u'IJ',
	ord(u'ᵫ'): u'ue',
}

def remove_ligatures(text):
	return text.translate(_LIGATURE_TRANSLATIONS)

################################################################################

_SPACES_PATTERN = re.compile(ur'\s+', re.U)
_EOL_PATTERN = re.compile(ur'[^\n\r]+', re.U)

def _replace_by_spaces(match):
	"""Replacement function that replaces all but \\n and \\r consecutive characters by one ASCII space."""
	return _EOL_PATTERN.sub(u' ', match.group(0))

def collapse_spaces(text):
	"""Collapse the consecutive non-end-of-line spaces character into one ASCII space.
	
	The characters \\n and \\r are the spaces characters that are considered as
	end-of-line characters.
	"""
	return _SPACES_PATTERN.sub(_replace_by_spaces, text)

################################################################################

def normalize_eol(text):
	"""Normalize the end-of-line characters to \\n."""
	return text.replace(u'\r\n', u'\n').replace(u'\r', u'\n')

################################################################################

