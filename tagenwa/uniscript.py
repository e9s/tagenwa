# -*- coding: UTF-8 -*-
"""
Unicode script helper functions

"""
__version__ = "0.1"
__license__ = "MIT"

from unicodedata import name
from codecs import open
from os.path import abspath, dirname, join as joinpath
import re

def islatin(text):
	"""Return True if all characters are latin and there is at least one character, False otherwise."""
	return len(text) and all(script(c) == 'LATIN' for c in text)


def block(c):
	"""Return the Unicode block name of the character.
	
	The data is based on the Unicode 5.1.0 database:
	http://www.unicode.org/Public/5.1.0/ucd/Blocks.txt
	
	:param c: single character
	:type c: unicode
	:return: block name
	:rtype: str
	:raise TypeError: if the argument is not a single unicode character.
	:raise KeyError: if the character block is not found.
	"""
	# assert argument is a single unicode character
	if not isinstance(c, unicode):
		raise TypeError('block() argument must be unicode, not '+repr(type(c)))
	if len(c) != 1:
		raise TypeError('block() argument must be a single unicode character')
	
	o = ord(c)
	for a, b, blockname in _UCD_BLOCKS:
		if a <= o <= b:
			return blockname
	raise KeyError('Unicode block not found.')


def script(c):
	"""Return the script of the character if known, None otherwise.
	
	The data is based on the Unicode 5.1.0 database:
	http://www.unicode.org/Public/5.1.0/ucd/Scripts.txt
	
	:param c: character
	:type c: unicode
	:return: script name
	:rtype: str
	:raise TypeError: if the argument is not a single unicode character
	:raise KeyError: if the character script is not found.
	"""
	# assert argument is a single unicode character
	if not isinstance(c, unicode):
		raise TypeError('block() argument must be unicode, not '+repr(type(c)))
	if len(c) != 1:
		raise TypeError('block() argument must be a single unicode character')
	
	o = ord(c)
	for a, b, scriptname in _UCD_SCRIPTS:
		if a <= o <= b:
			return scriptname
	raise KeyError('Unicode script not found.')


_ucd_pattern = re.compile(r'(?P<start>[0-9A-F]+)(?:\.\.(?P<end>[0-9A-F]+))? *;(?P<value>[^#]*)(?:#|\n)')
def _read_ucd_datafile(filename, folder='ucd510'):
	"""Read UCD data file."""
	filepath = joinpath(abspath(dirname(__file__)),folder,filename)
	data = []
	with open(filepath, 'rU', encoding='latin1') as f:
		for line in f:
			if line and not line.startswith('#'):
				match = _ucd_pattern.match(line)
				if match:
					start = int(match.group('start'),16)
					end = int(match.group('end'),16) if match.group('end') else start
					value = match.group('value').strip()
					data.append((start,end,value))
	return data

_UCD_BLOCKS = _read_ucd_datafile('Blocks.txt')
_UCD_SCRIPTS = _read_ucd_datafile('Scripts.txt')

from pprint import pprint
pprint(_UCD_BLOCKS)