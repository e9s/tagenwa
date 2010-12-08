# -*- coding: UTF-8 -*-
import unittest, doctest

from tagenwa.token import Token
from tagenwa.retokenizer.latin import StandardLatinRetokenizer



class TestStandardLatinRetokenizer(unittest.TestCase):
	
	def test_basic(self):
		retokenizer = StandardLatinRetokenizer()
		testcases = [
			([],[]),
			([u'abc'],[u'abc']),
			([u'ABC'],[u'abc']),
			([u'Abc'],[u'abc']),
		]
		for i,e in testcases:
			self.assertEqual(e, [token.text for token in retokenizer.retokenize([Token(t) for t in i])])
	
	def test_diacritics(self):
		retokenizer = StandardLatinRetokenizer()
		testcases = [
			([],[]),
			([u'aérien'],[u'aerien']),
			([u'ça'],[u'ca']),
		]
		for i,e in testcases:
			self.assertEqual(e, [token.text for token in retokenizer.retokenize([Token(t) for t in i])])
	
	def test_ligatures(self):
		retokenizer = StandardLatinRetokenizer()
		testcases = [
			([u'straß'],[u'strass']),
			([u'ex æquo'],[u'ex aequo']),
			([u'œuf'],[u'oeuf']),
			([u'Œuf'],[u'oeuf']),
			([u'vrĳ'],[u'vrij']),
		]
		for i,e in testcases:
			self.assertEqual(e, [token.text for token in retokenizer.retokenize([Token(t) for t in i])])



def suite():
	suite = unittest.TestLoader().loadTestsFromTestCase(TestStandardLatinRetokenizer)
	return suite

if __name__ == '__main__':
	unittest.main()