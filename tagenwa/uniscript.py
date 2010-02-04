# -*- coding: UTF-8 -*-
"""
Unicode script helper functions

"""
__version__ = "0.1"
__license__ = "MIT"


def islatin(text):
	"""Return True if all characters are latin and there is at least one character, False otherwise."""
	return len(text) and all(script(c) == u'latin' for c in text)


def script(c):
	"""Return the script type of the character if known, None otherwise.
	
	:param c: character
	:type c: unicode character
	:return: a unicode string representing the script
	:rtype: unicode or None
	"""
	o = ord(c)
	if o <= 0x02AF \
		or 0x1D00 <= o <= 0x1DBF \
		or 0x1E00 <= o <= 0x1EFF \
		or 0x2C60 <= o <= 0x2C7F \
		or 0xA720 <= o <= 0xA7FF \
		or 0xFB00 <= o <= 0xFB4F \
		or 0xFF01 <= o <= 0xFF5E:
		# see http://en.wikipedia.org/wiki/Latin_characters_in_Unicode
		# basic latin, latin supplement, latin extended A&B, IPA
		# phonetic extension
		# latin extended additional
		# latin extended C
		# latin extended D
		# fullwidth latin
		return u'latin'
	elif 0x0374 <= o <= 0x03FF:
		return u'greek'
	elif 0x0400 <= o <= 0x0523:
		return u'cyrillic'
	elif 0x0E00 <= o <= 0x0E7F:
		return u'thai'
	elif 0x4E00 <= o <= 0x9FFF  \
		or 0x3400 <= o <= 0x4DBF \
		or 0x20000 <= o <= 0x2A6DF \
		or 0x2A700 <= o <= 0x2B73F \
		or 0xF900 <= o <= 0xFAFF:
		#CJK, CJK A, CJK B, CJK C, CJK compatibility
		return u'cjk'
	elif 0x3040 <= o <= 0x309F:
		return u'hiragana'
	elif 0x30A0 <= o <= 0x30FF:
		return u'katakana'
	elif 0xAC00 <= o <= 0xD7AF:
		return u'hangul'
	else:
		return None
