# -*- coding: UTF-8 -*-
import re
from nltk.tokenize.treebank import TreebankWordTokenizer


class GenericTreebankWordTokenizer(TreebankWordTokenizer):
	"""A reimplementation of the nltk's TreebankWordTokenizer that also handles unicode."""
	
	_space_pattern = re.compile(r"\s+", re.U)
	
	_punctuation_patterns = [
		# Separate most punctuations and spaces
		re.compile(r"([^\w\.\-',&])", re.U),
		# Separate commas if they're followed by space.
		# (E.g., don't separate 2,500)
		re.compile(r"(,)(?=\W)", re.U),
		# Separate single quotes if they're preceded or followed by a non-word character.
		re.compile(r"(')(?=\W)", re.U),
		re.compile(r"(')(?=$)", re.U),
		re.compile(r"(?<=\W)(')", re.U),
		re.compile(r"(?<=^)(')", re.U),
		# Separate dashes (but not hyphens).
		re.compile(r"(\-{2,})", re.U),
		# Separate ellipses (but not dots).
		re.compile(r"(\.{2,})", re.U),
		# Separate periods that come before newline or end of string.
		re.compile(r"(\.+)\s*(?=\n|$)", re.U),
	]
	
	_quote_pattern = re.compile(r"(')", re.U)
	
	def span_tokenize_language(self, text, token_spans):
		token_spans = set()
		for match in self._quote_pattern.finditer(text):
			if match:
				token_spans.add(match.span(1))
		return token_spans
	
	
	def span_tokenize_between(self, text, token_spans):
		# Get the tokens between the found spans
		between_spans = set()
		i = 0
		for s,e in sorted(token_spans):
			if i != s:
				between_spans.add((i,s))
			i = e
		if e != len(text):
			between_spans.add((e,len(text)))
		return between_spans
	
	
	def span_tokenize(self, text, no_space=True):
		
		token_spans = set()
		for regexp in self._punctuation_patterns:
			for match in regexp.finditer(text):
				if match:
					token_spans.add(match.span(1))
		
		token_spans |= self.span_tokenize_language(text, token_spans)
		token_spans |= self.span_tokenize_between(text, token_spans)
		token_spans = sorted(token_spans)
		if no_space:
			token_spans = [(s,e) for s,e in token_spans if self._space_pattern.match(text[s:e]) is None]
		return token_spans
	
	def tokenize(self, text, **kwargs):
		return [text[s:e] for s,e in self.span_tokenize(text, **kwargs)]



class EnglishTreebankWordTokenizer(GenericTreebankWordTokenizer, TreebankWordTokenizer):
	
	def span_tokenize_language(self, text, token_spans):
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


def create_tokenizer(language):
	if language == u'en':
		return EnglishTreebankWordTokenizer()
	else:
		return GenericTreebankWordTokenizer()


for t in EnglishTreebankWordTokenizer().tokenize(u'A.B. 1..2 re-starts... a/b a\\c http://www.abc.com/ EUR1.234.567,45 (or $2.345,67) and goes on...'):
	print t.encode('utf-8')

for t in EnglishTreebankWordTokenizer().tokenize(u"""'When I'M a Duchess,' she said to herself, (not in a very hopeful tone
	though), 'I won't have any pepper in my kitchen AT ALL. Soup does very
	well without--Maybe it's always pepper that makes people hot-tempered,'... 0xAB657FF """):
	print t.encode('utf-8')