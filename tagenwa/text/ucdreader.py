# -*- coding: UTF-8 -*-
"""
Unicode character database (UCD) reader

"""
import codecs
from os.path import abspath, dirname, join as joinpath
import re



################################################################################
# UCD data file
################################################################################

def get_ucd_datafilepath(filename, folder=None):
	"""Return the filepath of the file in the correct data folder"""
	if folder is None:
		folder = 'ucd600'
	return joinpath(abspath(dirname(__file__)), '..', 'data', folder, filename)


################################################################################
# UCD data reader
################################################################################

## UCD data file regex pattern
_ucd_pattern = re.compile(r'(?P<start>[0-9A-F]+)(?:\.\.(?P<end>[0-9A-F]+))? *;(?P<value>[^#]*)(?:#|\n)')


def get_ucd_value(o, data, default=None):
	"""Get the value of the Unicode codepoint in the data or the default value if no entry found."""
	for a, b, value in data:
		if b >= o >= a:
			return value
	return default


def read_ucd_datafile(filename, folder=None, compact=False):
	"""Read UCD data file."""
	filepath = get_ucd_datafilepath(filename, folder)
	data = []
	with codecs.open(filepath, 'rU', encoding='latin1') as f:
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
		# Compact the consecutive entries with the same value into one entry
		# This reduces the number of keys and speed up the look up
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


################################################################################
# UCD Property value aliases
################################################################################

def read_property_value_aliases(properties=None, folder=None):
	filepath = get_ucd_datafilepath('PropertyValueAliases.txt', folder)
	aliases = {}
	property = None
	with codecs.open(filepath, 'rU', encoding='latin1') as f:
		for line in f:
			# Skip blank lines and comments
			if not line or line.startswith('#'):
				continue
			# Read the line
			fields = [field.strip() for field in line.split(u';')]
			# If defined, skip lines not in the 'properties' argument
			if properties and fields[0] not in properties:
				continue
			# Create a new property dictionary if needed
			if property != fields[0]:
				property = fields[0]
				if property not in aliases:
					aliases[property] = {}
			if fields[0] != u'ccc':
				if fields[1] != u'n/a':
					aliases[property][fields[1]] = fields[2]
			else:
				# TODO
				continue
	return aliases
	
	