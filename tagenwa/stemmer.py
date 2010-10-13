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
	imported_stemmer = True
	# supported languages by PyStemmer
	languages = ['da','de','en','es','fi','fr','hu','it','no','nl','pt','tr','sv']
	stemmers = dict((lang,Stemmer.Stemmer(lang)) for lang in languages)
except ImportError:
	imported_stemmer = False


def stem(token):
	"""Add the stem to the token.
	
	:param token: a token
	:type token: Token
	:return: a token with the stem if there is a stemmer for the token's language
	:rtype: Token
	"""
	# assert that PyStemmer is imported
	if not imported_stemmer:
		raise ImportError('Function stem(token) needs the PyStemmer module but this module could not be imported.')
	# check if a language is defined and supported and if the token is alphabetic word
	lang = token.get(u'lang')
	if lang is None or lang not in languages or not token.isword():
		return token
	# put the token in lower case
	low = token.text.lower()
	return token.set(u'stem', stemmers[lang].stemWord(low))


def stem_word(word, lang):
	"""Return the stem of a word.
	
	:param word: the word in lower case
	:type word: unicode
	:param lang: the two-letter iso 639-1 code of the language
	:param lang: unicode
	:rtype unicode
	"""
	# assert that PyStemmer is imported
	if not imported_stemmer:
		raise ImportError('Function stem(token) needs the PyStemmer module but this module could not be imported.')
	# check if a language is defined and supported
	if lang not in languages:
		raise KeyError('No stemmer exists for this language.')
	return stemmers[lang].stemWord(word)
	