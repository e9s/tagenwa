# -*- coding: UTF-8 -*-
"""
Snowball stemmers (wrapper around PyStemmer using the NLTK interface)

"""
__license__ = "MIT"

from nltk.stem.api import StemmerI


# Try to import PyStemmer
_STEMMERS = {}
try:
	import Stemmer
	# Supported languages by PyStemmer
	_PYSTEMMER_LANGUAGES = [
		u'da',u'de',u'en',u'es',u'fi',
		u'fr',u'hu',u'it',u'no',u'nl',
		u'pt',u'ro',u'ru',u'sv',u'tr',
	]
	_STEMMERS = dict((lang,Stemmer.Stemmer(lang)) for lang in _PYSTEMMER_LANGUAGES)
except ImportError:
	raise ImportError('The PyStemmer module could not be imported.')



class SnowballStemmer(StemmerI):
	
	def __init__(self, language):
		"""Create a Snowball stemmer for the specified language."""
		if language not in _PYSTEMMER_LANGUAGES:
			raise ValueError('Stemmer not defined for language %s' % language)
		self.language = language
		self._stemmer = _STEMMERS[language]
	
	
	def stem(self, token):
		"""Return the stem of the token using the Snowball algorithm."""
		return self._stemmer.stemWord(token.lower())



def get_stemmer(language):
	"""Create a new Snowball stemmer instance for the specified language."""
	return SnowballStemmer(language)
