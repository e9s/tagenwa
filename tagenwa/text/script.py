# -*- coding: UTF-8 -*-
"""
Unicode script helper functions

"""
from tagenwa.text.ucdreader import read_ucd_datafile, get_ucd_value, \
	get_ucd_datafilepath, read_property_value_aliases



def block(c, default=None):
	u"""Return the Unicode block name of the character or the default value if no block is found.
	
	The data is based on the Unicode 6.0.0 database:
	http://www.unicode.org/Public/6.0.0/ucd/Blocks.txt
	
	>>> block(u'a')
	u'Basic Latin'
	>>> block(u'_')
	u'Basic Latin'
	>>> block(u'é')
	u'Latin-1 Supplement'
	>>> script(u'β')
	u'Greek'
	>>> script(u'Ж')
	u'Cyrillic'
	>>> script(u'あ')
	u'Hiragana'
	>>> block(u'気')
	u'CJK Unified Ideographs'
	
	:param c: a single character
	:type c: unicode
	:param default: a default value
	:return: the block name or the default value
	:rtype: unicode
	:raise TypeError: if the argument is not a single unicode character.
	"""
	_assert_unicode_character(c)
	return get_ucd_value(ord(c), _UCD_BLOCKS, default)


def script(c, default=None):
	u"""Return the script name of the character or the default value if no script is found.
	
	The data is based on the Unicode 6.0.0 database:
	http://www.unicode.org/Public/6.0.0/ucd/Scripts.txt
	
	>>> script(u'a')
	u'Latin'
	>>> script(u'_')
	u'Common'
	>>> script(u'é')
	u'Latin'
	>>> script(u'β')
	u'Greek'
	>>> script(u'Ж')
	u'Cyrillic'
	>>> script(u'あ')
	u'Hiragana'
	>>> script(u'気')
	u'Han'
	
	:param c: a single character
	:type c: unicode
	:param default: a default value
	:return: the script name or the default value
	:rtype: unicode
	:raise TypeError: if the argument is not a single unicode character
	"""
	_assert_unicode_character(c)
	return get_ucd_value(ord(c), _UCD_SCRIPTS, default)


def script_extensions(c, default=None):
	_assert_unicode_character(c)
	o = ord(c)
	extensions = get_ucd_value(o, _UCD_SCRIPT_EXTENSIONS, None)
	if extensions is not None:
		return [_UCD_SCRIPT_ALIASES[e] for e in extensions.split(u' ')]
	return [get_ucd_value(o, _UCD_SCRIPTS, default)]


def tag_script(text):
	buffer = []
	previous = None
	for c in text:
		s = script(c)
		if s in (u'Common', None, u'Inherited'):
			if previous is not None:
				# Yield the character and the previous script
				yield (c, previous)
			else:
				# Script unknown, keep it in a buffer
				buffer.append((c, s))
		else:
			if buffer:
				# Yield the content of the buffer first
				for c0, s0 in buffer:
					yield (c0, s)
				buffer = []
			# Yield the character and the script
			yield (c, s)
			# Update the previous script
			previous = s
	for c0, s0 in buffer:
		yield (c0, s0)


################################################################################
# Helper functions
################################################################################

def _assert_unicode_character(c):
	"""Assert that the argument is a single unicode character"""
	if not isinstance(c, unicode):
		raise TypeError('Argument must be unicode, not '+repr(type(c)))
	if len(c) != 1:
		raise TypeError('Argument must be a single unicode character')


################################################################################
# Initializing functions
################################################################################

# initialize blocks and script database
_UCD_BLOCKS = read_ucd_datafile('Blocks.txt')
_UCD_SCRIPTS = read_ucd_datafile('Scripts.txt', compact=True)
_UCD_SCRIPT_EXTENSIONS = read_ucd_datafile('ScriptExtensions.txt', compact=True)
_UCD_SCRIPT_ALIASES = read_property_value_aliases(properties=[u'sc'])[u'sc']
