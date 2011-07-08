# -*- coding: UTF-8 -*-
import re
from nltk.tokenize.treebank import TreebankWordTokenizer

from tagenwa.text.script import tag_script


class GenericTreebankWordTokenizer(TreebankWordTokenizer):
	"""A reimplementation of the nltk's TreebankWordTokenizer that also handles unicode."""
	
	_SPACE_PATTERN = re.compile(r"\s+", re.U)
	
	_PUNCTUATION_PATTERNS = [
		# Separate most punctuations and spaces
		re.compile(r"([^\w\.\-',&])", re.U),
		# Separate commas if they're followed by space or end of string
		# (E.g., don't separate 2,500)
		re.compile(r"(,)(?=\W|$)", re.U),
		# Separate single quotes if they're preceded or followed by a non-word character.
		re.compile(r"(')(?=\W|$)", re.U),
		re.compile(r"(?<=\W)(')", re.U),
		re.compile(r"(?<=^)(')", re.U),
		# Separate dashes (but not hyphens).
		re.compile(r"(\-{2,})", re.U),
		# Separate ellipses (but not dots).
		re.compile(r"(\.{2,})", re.U),
		# Separate periods that come before newline or end of string.
		re.compile(r"(\.+)\s*(?=\n|$)", re.U),
	]
	
	_QUOTE_PATTERN = re.compile(r"(')", re.U)
	
	_SCRIPT_SPLITS = set([
		(u'Latin', u'Han'), (u'Han', u'Latin'),
		(u'Latin', u'Katakana'), (u'Katakana', u'Latin'),
		(u'Latin', u'Hiragana'), (u'Hiragana', u'Latin'),
	])
	
	
	def _span_tokenize_language(self, text, token_spans, **kwargs):
		"""Add language-specific tokens"""
		token_spans = set()
		for match in self._QUOTE_PATTERN.finditer(text):
			if match:
				token_spans.add(match.span(1))
		return token_spans
	
	
	def _span_tokenize_between(self, text, token_spans):
		"""Add spans between the found spans to cover the whole text"""
		
		# Add the spans between the found spans
		between_spans = set()
		i, end = 0, 0
		for start, end in sorted(token_spans):
			if i != start:
				between_spans.add((i, start))
			i = end
		
		# Add a last span to go until the end of the text
		if end != len(text):
			between_spans.add((end,len(text)))
		return between_spans
	
	
	def _span_tokenize_script(self, text, token_spans):
		"""Split the spans based on the script of the characters"""
		scripts = [s for c,s in tag_script(text)]
		script_spans = set()
		for start, end in token_spans:
			prev_end = start
			# For each span, split the span if the script transition dictates a split
			for i in xrange(start, end):
				if i+1 == end:
					script_spans.add((prev_end, end))
				elif (scripts[i], scripts[i+1]) in self._SCRIPT_SPLITS:
					script_spans.add((prev_end, i+1))
					prev_end = i+1
		return script_spans
	
	
	def span_tokenize(self, text, no_space=True, **kwargs):
		"""Return the spans for each token"""
		token_spans = set()
		for regexp in self._PUNCTUATION_PATTERNS:
			for match in regexp.finditer(text):
				if match:
					token_spans.add(match.span(1))
		
		token_spans |= self._span_tokenize_language(text, token_spans, **kwargs)
		token_spans |= self._span_tokenize_between(text, token_spans)
		token_spans = self._span_tokenize_script(text, token_spans)
		token_spans = sorted(token_spans)
		if no_space:
			token_spans = [(s,e) for s,e in token_spans if self._SPACE_PATTERN.match(text[s:e]) is None]
		return token_spans
	
	
	def tokenize(self, text, **kwargs):
		"""Tokenize the text"""
		return [text[s:e] for s,e in self.span_tokenize(text, **kwargs)]



class EnglishTreebankWordTokenizer(GenericTreebankWordTokenizer, TreebankWordTokenizer):
	
	def _span_tokenize_language(self, text, token_spans, **kwargs):
		token_spans = set()
		for regexp in self.CONTRACTIONS2:
			for match in regexp.finditer(text):
				if match:
					token_spans.add(match.span(2))
		for regexp in self.CONTRACTIONS3:
			for match in regexp.finditer(text):
				if match:
					token_spans.add(match.span(2))
					token_spans.add(match.span(3))
		return token_spans



def get_tokenizer(language):
	"""Create the tokenizer specific to the language if there is one
	or create a generic tokenizer.
	
	:param language: language code (ISO 631-1)
	:rtype language: unicode
	"""
	if language == u'en':
		return EnglishTreebankWordTokenizer()
	else:
		return GenericTreebankWordTokenizer()
