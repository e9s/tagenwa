# -*- coding: UTF-8 -*-
from unicodedata import combining as unicodedata_combining, normalize as unicodedata_normalize

# http://en.wikipedia.org/wiki/Alphabets_derived_from_the_Latin


def remove_accents(text):
	"""Remove all accents from the text.
	
	The string characters are decomposed using the Unicode's NFKD normalization
	and all the combining marks are removed.
	"""
	return u''.join(
		c for c in unicodedata_normalize('NFKD', text)
		if not unicodedata_combining(c)
	)


_NORMALIZING_TRANSLATIONS = {
	ord(u'ß'): u'ss',
	ord(u'æ'): u'ae',
	ord(u'œ'): u'oe',
	ord(u'ĳ'): u'ij',
}

def normalize_latin(text):
	return text.translate(_NORMALIZING_TRANSLATIONS)


class StandardLatinRetokenizer(object):
	
	def retokenize(self, tokens):
		"""Remove all diacritics and convert the text to lower case."""
		for token in tokens:
			text = normalize_latin(
				remove_accents(token.text).lower()
			)
			yield token.copy(text)

