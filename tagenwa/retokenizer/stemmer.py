# -*- coding: UTF-8 -*-
"""
Stemmer (interface around PyStemmer)

"""
__version__ = "0.1"
__license__ = "MIT"

from tagenwa.util.tools import copycase

try:
	# Try to import PyStemmer
	import Stemmer
	STEMMER_IS_IMPORTED = True
	# supported languages by PyStemmer
	STEMMER_LANGUAGES = ['da','de','en','es','fi','fr','hu','it','no','nl','pt','tr','sv']
	STEMMERS = dict((lang,Stemmer.Stemmer(lang)) for lang in STEMMER_LANGUAGES)
except ImportError:
	STEMMER_IS_IMPORTED = False


class StemmerRetokenizer(object):
	
	def __init__(self, lang=None, lang_key=u'lang', stem_key=u'stem'):
		"""Create a new retokenizer that will add the stem of word as a property of each token.
		
		:param lang: if not None, force the language used for the stemming
		:param lang_key: property key that contains the language of the token (if `lang` is None)
		:param stem_key: property key that will contain the stem of the token
		"""
		self.lang = lang
		self.lang_key = lang_key
		self.stem_key = stem_key
	
	def retokenize(self, tokens):
		"""Add the stem as a property of each token based on the language of the token.
		
		The language of the token must be specified with
		"""
		return (self._stem_token(t) for t in tokens)
	
	def _stem_token(self, token):
		lang = token.get(self.lang_key, None) if self.lang is None else self.lang
		if lang is None or lang not in STEMMER_LANGUAGES or not token.isword():
			return token
		word_lower = token.text.lower()
		return token.set(self.stem_key, STEMMERS[lang].stemWord(word_lower))


def stem(word, lang):
	"""Return the stem of a word.
	
	:param word: the word in lower case
	:type word: unicode
	:param lang: the two-letter iso 639-1 code of the language
	:param lang: unicode
	:rtype unicode
	"""
	# Assert that PyStemmer is imported
	if not STEMMER_IS_IMPORTED:
		raise ImportError('Function stem(token) needs the PyStemmer module but this module could not be imported.')
	# Check if a language is defined and supported
	if lang not in STEMMER_LANGUAGES:
		raise KeyError('No stemmer exists for this language.')
	return STEMMERS[lang].stemWord(word)

