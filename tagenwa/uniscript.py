# -*- coding: UTF-8 -*-
"""
Unicode script helper functions

"""
__version__ = "0.1"
__license__ = "MIT"

from tagenwa.util.tools import memoize, group_count

from unicodedata import name
from codecs import open
from os.path import abspath, dirname, join as joinpath
import re
import cPickle


def block(c, default=None):
	u"""Return the Unicode block name of the character or the default value if no block is found.
	
	The data is based on the Unicode 5.1.0 database:
	http://www.unicode.org/Public/5.1.0/ucd/Blocks.txt
	
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
	
	return _get_ucd_value(ord(c), _UCD_BLOCKS, default)



def script(c, default=None, avoid_common=False):
	u"""Return the script name of the character or the default value if no script is found.
	
	The data is based on the Unicode 5.1.0 database:
	http://www.unicode.org/Public/5.1.0/ucd/Scripts.txt
	
	If the parameter `avoid_common` is set to True, the `script` function tries to avoid to return the value "Common"
	by returning for the script name of the majority of the character within the same block as the character `c`.
	Note that this script name may still be "Common".
	
	>>> script(u'a')
	u'Latin'
	>>> script(u'_')
	u'Common'
	>>> script(u'_', avoid_common = True)
	u'Latin'
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
	:param avoid_common: if True, try to replace the return value 'Common' by the majority script of the containing block
	:type c: bool
	:return: the script name or the default value
	:rtype: unicode
	:raise TypeError: if the argument is not a single unicode character
	"""
	_assert_unicode_character(c)
	
	# search script name in the database
	scriptname = _get_ucd_value(ord(c), _UCD_SCRIPTS, default)
	
	# replace common by the majority script of the block, if needed
	if scriptname == u'Common' and avoid_common:
		majority = _MAJORITY_SCRIPTS[block(c)]
		return majority if majority else u'Common'
	
	return scriptname



def _assert_unicode_character(c):
	"""Assert that the argument is a single unicode character"""
	if not isinstance(c, unicode):
		raise TypeError('Argument must be unicode, not '+repr(type(c)))
	if len(c) != 1:
		raise TypeError('Argument must be a single unicode character')



def _get_ucd_value(o, data, default=None):
	"""Get the value of the Unicode codepoint in the data or the default value if no entry found."""
	for a, b, value in data:
		if a <= o <= b:
			return value
	return default


################################################################################
# Initializing functions
################################################################################

"""UCD data file regex pattern"""
_ucd_pattern = re.compile(r'(?P<start>[0-9A-F]+)(?:\.\.(?P<end>[0-9A-F]+))? *;(?P<value>[^#]*)(?:#|\n)')


def _read_ucd_datafile(filename, folder='ucd510', compact=False):
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
	data.sort()
	if compact:
		#  compact the consecutive entries with the same value into one entry
		compacted = []
		iterator = iter(data)
		buffer = iterator.next()
		for d in iterator:
			if buffer[2] == d[2] and buffer[1]+1 == d[0]:
				buffer = (buffer[0], d[1], buffer[2])
			else:
				compacted.append(buffer)
				buffer = d
		return compacted
	return data


# initialize blocks and script database
_UCD_BLOCKS = _read_ucd_datafile('Blocks.txt')
_UCD_SCRIPTS = _read_ucd_datafile('Scripts.txt', compact=True)



def _get_majority_scripts(folder='ucd510'):
	"""Return the majority script of each block (by calculating or unpickling it)."""
	filepath = joinpath(abspath(dirname(__file__)),folder,'BlockScripts.cache.txt')
	try:
		# read majority dictionary if it exists
		return cPickle.load(open(filepath,'rt'))
	except:
		# count scripts by block
		script_count_by_block = dict(
			(
				block,
				group_count(_get_ucd_value(i, _UCD_SCRIPTS) for i in xrange(start, end+1))
			)
			for (start,end,block) in _UCD_BLOCKS
		)
		# remove script = None
		for block in script_count_by_block:
			if None in script_count_by_block[block]:
				del script_count_by_block[block][None]
		
		# modify 'Common' to <blank> to put it last in case of ex-aequo
		majority = dict(
			(
				block,
				max((v,k if k != u'' else None) for (k,v) in counts.iteritems())[1] if counts else None
			)
			for (block,counts) in script_count_by_block.iteritems()
		)
		# put back <blank> as 'Common'
		for k in majority:
			if majority[k] == u'':
				majority[k] = u'Common'
		# correct basic latin (too many common and control characters)
		majority['Basic Latin'] = u'Latin'
		
		# save majority dictionary
		cPickle.dump(majority, open(filepath,'wt'))
		return majority


# initialize majority script of each block
_MAJORITY_SCRIPTS = _get_majority_scripts()