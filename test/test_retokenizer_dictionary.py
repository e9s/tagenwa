# -*- coding: UTF-8 -*-
import unittest, doctest

from tagenwa.token import Token
from tagenwa.retokenizer.dictionary import DictionaryRetokenizer

class TestDictionaryRetokenizer(unittest.TestCase):
	
	def setUp(self):
		self.retokenizer = DictionaryRetokenizer()
		self.retokenizer.add(
			[u'hello'],
			[Token(u'HELLO')]
		)
		self.retokenizer.add(
			[u'good',u'morning'],
			[Token(u'GOOD'), Token(u'MORNING')]
		)
		pass
	
	def test_simple(self):
		testcases = [
			([],[]),
			([u'abc'],[u'abc']),
			([u'hello'],[u'HELLO']),
			([u'abc', u'hello'],[u'abc', u'HELLO']),
			([u'hello', u'xyz'],[u'HELLO', u'xyz']),
			([u'abc', u'hello', u'xyz'],[u'abc', u'HELLO', u'xyz']),
		]
		for i,e in testcases:
			self.assertEqual(e, [token.text for token in self.retokenizer.retokenize([Token(t) for t in i])])
	
	def test_compound(self):
		testcases = [
			([],[]),
			([u'abc'],[u'abc']),
			([u'good',u'morning'],[u'GOOD',u'MORNING']),
			([u'abc', u'good',u'morning'],[u'abc', u'GOOD',u'MORNING']),
			([u'good',u'morning', u'xyz'],[u'GOOD',u'MORNING', u'xyz']),
			([u'abc', u'good',u'morning', u'xyz'],[u'abc', u'GOOD',u'MORNING', u'xyz']),
			([u'abc', u'good', u'xyz'],[u'abc', u'good', u'xyz']),
			([u'abc', u'morning', u'xyz'],[u'abc', u'morning', u'xyz']),
		]
		for i,e in testcases:
			self.assertEqual(e, [token.text for token in self.retokenizer.retokenize([Token(t) for t in i])])


def suite():
	suite = unittest.TestLoader().loadTestsFromTestCase(TestDictionaryRetokenizer)
	return suite

if __name__ == '__main__':
	unittest.main()