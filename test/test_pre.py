# -*- coding: UTF-8 -*-
import unittest, doctest

from tagenwa.pre import tokenize


class TestPre(unittest.TestCase):
	
	def test_pre_doctest(self):
		import tagenwa.pre
		failure_count, test_count = doctest.testmod(tagenwa.pre)
		self.assertEqual(failure_count, 0, 'Testing doctest from tagenwa.pre: %i failed out of %i' % (failure_count, test_count))
	
	def test_tokenize_empty(self):
		testcases = [
			(u'', []),
			(u' ', [u' ']),
			(u'   ', [u' ']),
			(u'\n', [u'\n']),
			#(u'\r', [u'\n']),
			#(u'\r\n', [u'\n']),
			(u'\n\n\n', [u'\n\n\n']),
		]
		for (i,e) in testcases:
			self.assertEqual(e, list(unicode(t) for t in tokenize(i)))
	
	def test_tokenize_latin(self):
		testcases = [
			(u'Lowercase',         [u'Lowercase']),
			(u'UPPERCASE',         [u'UPPERCASE']),
			(u'some English text', [u'some', u' ', u'English', u' ', u'text']),
			(u'texte en français', [u'texte', u' ', u'en', u' ', u'français']),
		]
		for (i,e) in testcases:
			self.assertEqual(e, list(unicode(t) for t in tokenize(i)))
	
	def test_tokenize_japanese(self):
		testcases = [
			(u'日本語で書いている文',        [u'日本語', u'で', u'書', u'いている', u'文']),
			(u'日本語とEnglishの文',     [u'日本語', u'と', u'English', u'の', u'文']),
			(u'ひらがなカタカナ漢字',        [u'ひらがな', u'カタカナ', u'漢字']),
			# test half-width latin character
			(u'aａa',               [u'aａa']),
			# test half-width katakana
			(u'ｶﾀｶﾅカタカナ',            [u'ｶﾀｶﾅカタカナ']),
			# test the katakana "chou'onpu" (not hyphen/dash!)
			(u'ハロー',               [u'ハロー']),
		]
		for (i,e) in testcases:
			self.assertEqual(e, list(unicode(t) for t in tokenize(i)))
	
	def test_tokenize_japanese_nfkc(self):
		testcases = [
			(u'日本語で書いている文',        [u'日本語', u'で', u'書', u'いている', u'文']),
			(u'日本語とEnglishの文',     [u'日本語', u'と', u'English', u'の', u'文']),
			(u'ひらがなカタカナ漢字',        [u'ひらがな', u'カタカナ', u'漢字']),
			# test half-width latin character
			(u'aａa',               [u'aaa']),
			# test half-width katakana
			(u'ｶﾀｶﾅカタカナ',            [u'カタカナカタカナ']),
			# test the katakana "chou'onpu" (not hyphen/dash!)
			(u'ハロー',               [u'ハロー']),
		]
		for (i,e) in testcases:
			self.assertEqual(e, list(unicode(t) for t in tokenize(i, normalization_form='NFKC')))
	
	def test_tokenize_combining_marks(self):
		testcases = [
			# see http://www.unicode.org/reports/tr15/images/UAX15-NormFig5.jpg
			(u'mmm\u1E69mmm',             [u'mmm\u1E69mmm']),
			(u'mmms\u0307\u0323mmm',      [u'mmm\u1E69mmm']),
			(u'mmms\u0323\u0307mmm',      [u'mmm\u1E69mmm']),
			(u'mmm\u1E0B\u0323mmm',       [u'mmm\u1E0D\u0307mmm']),
			(u'mmm\u0071\u0307\u0323mmm', [u'mmm\u0071\u0323\u0307mmm']),
		]
		for (i,e) in testcases:
			self.assertEqual(e, list(unicode(t) for t in tokenize(i)))
	
	def test_tokenizer_indic(self):
		testcases = [
			# Devanagari ka - Devanagari virama (= halant) - Devanagari ya - Devanagari  aa
			(u'\u0915\u094D\u092F\u093E',      [u'\u0915\u094D\u092F\u093E']),
			# with ZWJ after the virama
			(u'\u0915\u094D\u200D\u092F\u093E',      [u'\u0915\u094D\u200D\u092F\u093E']),
			# with ZWNJ after the virama
			(u'\u0915\u094D\u200C\u092F\u093E',      [u'\u0915\u094D\u200C\u092F\u093E']),
		]
		for (i,e) in testcases:
			self.assertEqual(e, list(unicode(t) for t in tokenize(i)))
	
	def test_tokenizer_zero_width(self):
		testcases = [
			# test zero-width space
			(u'AAA\u200bAAA',      [u'AAA', u' ', u'AAA']),
			# test zero-width non-joiner (ZWNJ) character
			(u'auf\u200cfinden',   [u'auf\u200cfinden']),
			# test zero-width joiner (ZWJ) character
			(u'AAA\u200dAAA',      [u'AAA\u200dAAA']),
		]
		for (i,e) in testcases:
			self.assertEqual(e, list(unicode(t) for t in tokenize(i)))
	
	def test_tokenize_numbers(self):
		testcases = [
			# test numbers
			(u'a01',               [u'a01']),
			(u'a_01',              [u'a_01']),
			(u'+555',              [u'+', u'555']),
			(u'-555',              [u'-', u'555']),
			(u'$555',              [u'$', u'555']),
			(u'1.05',              [u'1', u'.', u'05']),
		]
		for (i,e) in testcases:
			self.assertEqual(e, list(unicode(t) for t in tokenize(i)))
	
	def test_tokenize_punctuations(self):
		testcases = [
			# test punctuation
			(u'comma, dot.',       [u'comma', u',', u' ', u'dot', u'.']),
			(u'triple... dots',    [u'triple', u'.', u'.', u'.', u' ', u'dots']),
			(u'読点、句点。',            [u'読点', u'、', u'句点', u'。']),
			(u'※米印、こめじるし',         [u'※', u'米印', u'、', u'こめじるし']),
			(u'こめ※じるし',         [u'こめ', u'※', u'じるし']),
			(u'under_score',       [u'under_score']),
			(u'hy-phen',           [u'hy',u'-',u'phen']),
			(u'pl+us',             [u'pl',u'+',u'us']),
			(u'sla/sh',            [u'sla',u'/',u'sh']),
			(u'st*ar',             [u'st',u'*',u'ar']),
			# test sequence of punctuations
			(u'***',               [u'*', u'*', u'*']),
			(u'+=',                [u'+', u'=']),
			(u'-=',                [u'-', u'=']),
			(u'.=',                [u'.', u'=']),
			(u',=',                [u',', u'=']),
			# test quotes
			(u'\'."',              [u"'", u'.', u'"']),
			(u'"quotes"',          [u'"', u'quotes', u'"']),
			(u"simple'quote",      [u'simple', u"'", u'quote']),
			# test opening and closing punctuations
			(u'(parens)',          [u'(', u'parens', u')']),
			(u"f((x,y),z)",        [u'f', u'(', u'(', u'x', u',', u'y', u')', u',', u'z', u')']),
		]
		for (i,e) in testcases:
			self.assertEqual(e, list(unicode(t) for t in tokenize(i)))
	
	def test_tokenize_punctuation_dash(self):
		testcases = [
			(u'hy-phen',           [u'hy',u'-',u'phen']),
			# test beginning and ending dashes
			(u'---hello---',       [u'-', u'-', u'-',u'hello',u'-', u'-', u'-']),
			(u'-hello',            [u'-',u'hello']),
			(u'hello-',            [u'hello',u'-']),
			(u'-hello-',           [u'-',u'hello',u'-']),
			(u'--..--',            [u'-', u'-', u'.', u'.', u'-', u'-']),
		]
		for (i,e) in testcases:
			self.assertEqual(e, list(unicode(t) for t in tokenize(i)))
	
	def test_tokenize_text(self):
		testcases = [
			(u'Hello,\nGoodbye.',    [u'Hello',u',',u'\n',u'Goodbye',u'.']),
			(u'Hello,\n\nGoodbye.',  [u'Hello',u',',u'\n\n',u'Goodbye',u'.']),
			(u'Hello,  \nGoodbye.',  [u'Hello',u',',u' ',u'\n',u'Goodbye',u'.']),
			# test space collapsing
			(u'Hello, Goodbye.',     [u'Hello',u',',u' ',u'Goodbye',u'.']),
			(u'Hello,    Goodbye.',  [u'Hello',u',',u' ',u'Goodbye',u'.']),
			(u'Hello,\tGoodbye.',    [u'Hello',u',',u' ',u'Goodbye',u'.']),
			(u'Hello,\t\tGoodbye.',  [u'Hello',u',',u' ',u'Goodbye',u'.']),
			(u'Hello, \tGoodbye.',   [u'Hello',u',',u' ',u'Goodbye',u'.']),
			(u'Hello, \t\tGoodbye.', [u'Hello',u',',u' ',u'Goodbye',u'.']),
		]
		for (i,e) in testcases:
			self.assertEqual(e, list(unicode(t) for t in tokenize(i)))


def suite():
	suite = unittest.TestLoader().loadTestsFromTestCase(TestPre)
	return suite

if __name__ == '__main__':
	unittest.main()