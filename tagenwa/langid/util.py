# -*- coding: UTF-8 -*-
"""
Useful functions for language identification

"""
__version__ = "0.1"
__license__ = "MIT"


def set_lang(tokens, lang):
	"""Set the language of the iterable of tokens.
	
	:param tokens: iterable of tokens
	:type tokens: iterable
	:param lang: language (ISO 639 language code)
	:type lang: unicode
	:return: iterable of tokens with the property "lang" set to `lang` 
	:rtype: iterable
	"""
	return (t.set(u'lang',lang) for t in tokens)

