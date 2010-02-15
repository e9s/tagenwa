# -*- coding: UTF-8 -*-
"""
Language identifier for several European languages
written in the latin alphabet

"""
__version__ = "0.1"
__license__ = "MIT"

from tagenwa.pre import tokenize
from tagenwa.langid import trigrams, NGramHMMLanguageIdentifier

from itertools import chain
from os.path import dirname, abspath, join as joinpath, isfile
from os import listdir
from codecs import open
import cPickle

"""Known languages
"""
languages = ['de','en','es','fr','it','nl','pt']


def _train(identifier):
	folderpath = joinpath(abspath(dirname(__file__)),'eulangid_training')
	for name in listdir(folderpath):
		# skip folders
		if not isfile(joinpath(folderpath,name)):
			continue
		
		# get the language
		lang = name[:2].lower()
		if lang not in languages or name[2] != '_':
			continue
		
		# process the file
		f = open(joinpath(folderpath,name), 'rt', 'utf-8')
		tokens = []
		for line in f:
			# put the text in lower case
			# underscore is often used to mark italics in Project Gutenberg's texts
			# so we replace them by spaces
			text = line.replace(u'_', u' ').strip().lower()
			
			# pre-tokenize and filter for words
			if text:
				tokens = chain(tokens, (t0 for t0 in tokenize(text) if t0.isword()))
		# train the whole file
		identifier.train(tokens, lang)
		# close the file
		f.close()
	return identifier

def _load(filepath=None):
	if filepath is None:
		filepath = joinpath(abspath(dirname(__file__)),'eulangid.cache.txt')
	return cPickle.load(open(filepath,'rt'))

def _save(identifier, filepath=None):
	if filepath is None:
		filepath = joinpath(abspath(dirname(__file__)),'eulangid.cache.txt')
	cPickle.dump(identifier, open(filepath,'wt'))

try:
	identifier = _load()
except:
	identifier = NGramHMMLanguageIdentifier()
	identifier = _train(identifier)
	_save(identifier)
