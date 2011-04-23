# -*- coding: UTF-8 -*-
import tagenwa.langid.ngram as ngram

import unittest, doctest


class TestTokenize(unittest.TestCase):
	
	def test_space(self):
		testcases = [
			(u'', []),
			(u' ', [u' ']),
			(u'  ', [u'  ']),
			(u'  \n\n  ', [u'  \n\n  ']),
		]
		for i,e in testcases:
			self.assertEqual(e, ngram.tokenize(i))
	
	
	def test_latin(self):
		testcases = [
			(u'', []),
			(u'hello', [u'hello']),
			(u'hello world', [u'hello', u' ', u'world']),
			(u'abc123 45', [u'abc123', u' ', u'45']),
			(u'abc123+45', [u'abc123', u'+', u'45']),
			(u' +123.45', [u' ', u'+', u'123', u'.', u'45']),
		]
		for i,e in testcases:
			self.assertEqual(e, ngram.tokenize(i))
	
	
	def test_latin_japanese(self):
		testcases = [
			(
				u'今日John Smith氏は会議に出ました。',
				[u'今日', u'John', u' ', u'Smith', u'氏は会議に出ました', u'。']
			),
		]
		for i,e in testcases:
			self.assertEqual(e, ngram.tokenize(i))



class TestNgram(unittest.TestCase):
	
	def test_ngram_doctest(self):
		failure_count, test_count = doctest.testmod(ngram)
		self.assertEqual(failure_count, 0, 'Testing doctest from tagenwa.langid.ngram: %i failed out of %i' % (failure_count, test_count))


def suite():
	suite = unittest.TestSuite([
		unittest.TestLoader().loadTestsFromTestCase(TestTokenize),
		unittest.TestLoader().loadTestsFromTestCase(TestNgram),
	])
	suite = unittest.TestLoader().loadTestsFromTestCase(TestNgram)
	return suite

if __name__ == '__main__':
	unittest.main()
