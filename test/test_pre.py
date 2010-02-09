# -*- coding: UTF-8 -*-
import unittest

from tagenwa.pre import tokenize

class TestPre(unittest.TestCase):
	
	def test_tokenize_empty(self):
		testcases = [
			(u'', []),
			(u' ', []),
			(u'   ', []),
			(u'\n', []),
			(u'\r', []),
			(u'\n\n\n', []),
		]
		for (i,e) in testcases:
			self.assertEqual(e, list(unicode(t) for t in tokenize(i)))
	
	def test_tokenize_letters(self):
		testcases = [
			(u'Lowercase',         [u'Lowercase']),
			(u'UPPERCASE',         [u'UPPERCASE']),
			(u'some English text', [u'some', u' ', u'English', u' ', u'text']),
			(u'texte en français', [u'texte', u' ', u'en', u' ', u'français']),
			(u'日本語で書いている文',        [u'日本語', u'で', u'書', u'いている', u'文']),
			(u'日本語とEnglishの文',     [u'日本語', u'と', u'English', u'の', u'文']),
			(u'ひらがなカタカナ漢字',        [u'ひらがな', u'カタカナ', u'漢字']),
			# test half-width latin character
			(u'aａa',               [u'aaa']),
			# test half-width katakana
			(u'ｶﾀｶﾅカタカナ',            [u'カタカナカタカナ']),
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
			(u'triple... dots',    [u'triple', u'...', u' ', u'dots']),
			(u'読点、句点。',            [u'読点', u'、', u'句点', u'。']),
			(u'※米印、こめじるし',         [u'※', u'米印', u'、', u'こめじるし']),
			(u'こめ※じるし',         [u'こめ', u'※', u'じるし']),
			(u'under_score',       [u'under_score']),
			(u'hy-phen',           [u'hy-phen']),
			(u'pl+us',             [u'pl',u'+',u'us']),
			(u'sla/sh',            [u'sla',u'/',u'sh']),
			(u'st*ar',             [u'st',u'*',u'ar']),
			# test beginning and ending dashes
			(u'---hello---',       [u'---',u'hello',u'---']),
			(u'-hello',            [u'-',u'hello']),
			(u'hello-',            [u'hello',u'-']),
			(u'-hello-',           [u'-',u'hello',u'-']),
			(u'-',                 [u'-']),
			(u'--',                [u'--']),
			(u'---',               [u'---']),
			(u'----',              [u'----']),
			(u'--..--',            [u'--',u'..',u'--']),
			# test sequence of punctuations
			(u'***',               [u'***']),
			(u'+=',                [u'+=']),
			(u'-=',                [u'-',u'=']),
			(u'.=',                [u'.',u'=']),
			(u',=',                [u',',u'=']),
			# test the katakana "chou'onpu" (not hyphen/dash!)
			(u'ハロー',               [u'ハロー']),
			# test quotes
			(u'"quotes"',          [u'"', u'quotes', u'"']),
			(u"simple'quote",      [u'simple', u"'", u'quote']),
			# test opening and closing punctuations
			(u'(parens)',          [u'(', u'parens', u')']),
			(u"f((x,y),z)",        [u'f', u'((', u'x', u',', u'y', u')', u',', u'z', u')']),
		]
		for (i,e) in testcases:
			self.assertEqual(e, list(unicode(t) for t in tokenize(i)))
	
	def test_tokenize_patterns(self):
		testcases = [
			# test patterns
			(u"2009/12/31",        [u'2009', u'/', u'12', u'/', u'31']),
			# TODO: presplit abbreviations, numbers (with comma or dot), urls or e-mails?
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