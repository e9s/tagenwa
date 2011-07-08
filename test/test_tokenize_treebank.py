# -*- coding: UTF-8 -*-
import nltk
import unittest, doctest
import unicodedata
from tagenwa.tokenize.treebank import GenericTreebankWordTokenizer, EnglishTreebankWordTokenizer



class TestTreebankWordTokenizer(unittest.TestCase):
	
	tokenizer_classes = [
		GenericTreebankWordTokenizer,
		EnglishTreebankWordTokenizer,
	]
	
	
	def test_doctest(self):
		import tagenwa.tokenize.treebank
		failure_count, test_count = doctest.testmod(tagenwa.tokenize.treebank)
		self.assertEqual(failure_count, 0, 'Testing doctest from tagenwa.tokenize.treebank: %i failed out of %i' % (failure_count, test_count))
	
	
	def test_tokenize_spaces(self):
		testcases = [
			(u'',       []),
			(u' ',      [u' ']),
			(u'   ',    [u' ', u' ', u' ']),
			(u'\n',     [u'\n']),
			(u'\n\n\n', [u'\n', u'\n', u'\n']),
		]
		for tclass in self.tokenizer_classes:
			tokenizer = tclass()
			for (i,e) in testcases:
				self.assertEqual([], list(unicode(t) for t in tokenizer.tokenize(i)))
				self.assertEqual(e, list(unicode(t) for t in tokenizer.tokenize(i, no_space=False)))
	
	
	def test_number(self):
		testcases = [
			(u'a01',                [u'a01']),
			(u'a_01',               [u'a_01']),
			(u'+555.55',            [u'+', u'555.55']),
			(u'-555.55',            [u'-555.55']),
			(u'$555.55',            [u'$', u'555.55']),
			(u'$2,555.55',          [u'$', u'2,555.55']),
			(u'1,000,000',          [u'1,000,000']),
			(u'1,000,000 is a lot', [u'1,000,000', u'is', u'a', u'lot']),
			(u'1,000,000, a lot',   [u'1,000,000', u',', u'a', u'lot']),
		]
		for tclass in self.tokenizer_classes:
			tokenizer = tclass()
			for (i,e) in testcases:
				self.assertEqual(e, list(unicode(t) for t in tokenizer.tokenize(i)))
	
	
	def test_tokenize_quotes(self):
		testcases = [
			(u"'",              [u"'"]),
			(u"'abc'",          [u"'", u'abc', u"'"]),
			(u"he said:'abc'.", [u"he", u"said", u":", u"'", u'abc', u"'", u"."]),
		]
		for tclass in self.tokenizer_classes:
			tokenizer = tclass()
			for (i,e) in testcases:
				self.assertEqual(e, list(unicode(t) for t in tokenizer.tokenize(i)))
	
	
	def test_tokenizer_zero_width(self):
		testcases = [
			# test zero-width space
			(u'XXX\u200bYYY',      [u'XXX', u'YYY']),
			# test zero-width non-joiner (ZWNJ) character
			(u'auf\u200cfinden',   [u'auf\u200cfinden']),
			# test zero-width joiner (ZWJ) character
			(u'AAA\u200dAAA',      [u'AAA\u200dAAA']),
		]
		for tclass in self.tokenizer_classes:
			tokenizer = tclass()
			for (i,e) in testcases:
				self.assertEqual(e, list(unicode(t) for t in tokenizer.tokenize(i)))
	
	
	def test_tokenizer_han(self):
		testcases = [
			# test zero-width space
			(u'abc漢字def',      [u'abc', u'漢字', u'def']),
			(u'abc漢字 def',     [u'abc', u'漢字', u'def']),
			(u'abc漢字def',      [u'abc', u'漢字', u'def']),
			(u'abc 漢字 def',    [u'abc', u'漢字', u'def']),
			(u'abc漢字',         [u'abc', u'漢字']),
			(u'漢字def',         [u'漢字', u'def']),
		]
		for tclass in self.tokenizer_classes:
			tokenizer = tclass()
			for (i,e) in testcases:
				self.assertEqual(e, list(unicode(t) for t in tokenizer.tokenize(i)))
	
	
	def test_tokenizer_indic(self):
		testcases = [
			# Devanagari ka - Devanagari virama (= halant) - Devanagari ya - Devanagari  aa
			(u'\u0915\u094D\u092F\u093E',      [u'\u0915\u094D\u092F\u093E']),
			# with ZWJ after the virama
			(u'\u0915\u094D\u200D\u092F\u093E',      [u'\u0915\u094D\u200D\u092F\u093E']),
			# with ZWNJ after the virama
			(u'\u0915\u094D\u200C\u092F\u093E',      [u'\u0915\u094D\u200C\u092F\u093E']),
		]
		for tclass in self.tokenizer_classes:
			tokenizer = tclass()
			for (i,e) in testcases:
				self.assertEqual(e, list(unicode(t) for t in tokenizer.tokenize(i)))



class TestEnglishTreebankWordTokenizer(unittest.TestCase):
	
	def test_share(self):
		shares = u"""A&B shares are being traded at $1,234.50 (1.8%) on the N.Y.S.E."""
		tokenizer = EnglishTreebankWordTokenizer()
		self.assertEqual(
			tokenizer.tokenize(shares),
			[
				"A&B", "shares", "are", "being", "traded", "at", "$", "1,234.50", "(", "1.8", "%", ")",
				"on", "the", "N.Y.S.E", u".",
			]
		)
	
	def test_alice(self):
		# http://nltk.googlecode.com/svn/trunk/doc/book/ch03.html
		alice1 = u"""'When I'M a Duchess,' she said to herself, (not in a very hopeful tone
		though), 'I won't have any pepper in my kitchen AT ALL."""
		alice2 = u"""Soup does very well without--Maybe it's always pepper that makes people hot-tempered,'..."""
		
		tokenizer = EnglishTreebankWordTokenizer()
		
		self.assertEqual(
			tokenizer.tokenize(alice1),
			[
				"'", "When", "I", "'M", "a", "Duchess", ",", "'", "she", "said", "to", "herself", ",",
				"(", "not", "in", "a", "very", "hopeful", "tone", "though", ")", ",",
				"'", "I", "wo", "n't", "have", "any", "pepper", "in", "my", "kitchen", "AT", "ALL", ".",
			]
		)
		self.assertEqual(
			tokenizer.tokenize(alice2),
			[
				"Soup", "does", "very", "well", "without",
				"--", "Maybe", "it", "'s", "always", "pepper", "that", "makes", "people", "hot-tempered", ",", "'", "..."
			]
		)



def suite():
	suite = unittest.TestSuite([
		unittest.TestLoader().loadTestsFromTestCase(TestTreebankWordTokenizer),
		unittest.TestLoader().loadTestsFromTestCase(TestEnglishTreebankWordTokenizer),
	])
	return suite

if __name__ == '__main__':
	unittest.main()	
