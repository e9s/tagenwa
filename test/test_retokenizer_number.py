# -*- coding: UTF-8 -*-
import unittest, doctest

from tagenwa.token import Token
from tagenwa.retokenizer.number import NumberRetokenizer

class TestNumberRetokenizer(unittest.TestCase):
	
	def test_no_number(self):
		testcases = [
			[],
			[u'Lorem'],
			[u'Lorem', u'ipsum'],
			[u'Lorem', u'ipsum', u'sic', u'dolor', u'amet', u',', u'consectetur', u'adipisicing', u'elit', u'.'],
		]
		retokenizer = NumberRetokenizer()
		for i in testcases:
			self.assertEqual(i, [token.text for token in retokenizer.retokenize([Token(t) for t in i])])
	
	def test_number(self):
		testcases = [
			([u'123', u'456'], [u'123456']),
			([u'3', u'.', u'5'], [u'3.5']),
			([u'3', u',', u'5'], [u'3,5']),
			([u'1', u',', u'234', u'.', u'00'], [u'1,234.00']),
			([u'3', u'.', u'5', u' ', u'kg'], [u'3.5', u' ', u'kg']),
			([u'-', u'3', u'.', u'5', u' ', u'kg'], [u'-', u'3.5', u' ', u'kg']),
		]
		retokenizer = NumberRetokenizer()
		for i,e in testcases:
			self.assertEqual(e, [token.text for token in retokenizer.retokenize([Token(t) for t in i])])
	
	def test_almost_number(self):
		testcases = [
			[u'3', u'.'],
			[u'3', u'.', u'b'],
			[u'3', u'.', u'.', u'.'],
			[u'a', u'3', u'.'],
			[u'a', u'3', u'.', u'b'],
			[u'a', u'3', u'.', u'b'],
		]
		retokenizer = NumberRetokenizer()
		for i in testcases:
			self.assertEqual(i, [token.text for token in retokenizer.retokenize([Token(t) for t in i])])
	
	def test_token_property(self):
		testcases = [
			([u'3', u'.', u'5'], [Token(u'3.5').set('pos', 'CD')]),
			([u'a', u'3', u'.'], [Token(u'a'), Token(u'3').set('pos', 'CD'), Token(u'.')]),
		]
		retokenizer = NumberRetokenizer(token_key='pos', token_value='CD')
		for i,e in testcases:
			self.assertEqual(e, list(retokenizer.retokenize([Token(t) for t in i])))
	


def suite():
	suite = unittest.TestLoader().loadTestsFromTestCase(TestNumberRetokenizer)
	return suite
	

if __name__ == '__main__':
	unittest.main()