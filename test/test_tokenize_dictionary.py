# -*- coding: UTF-8 -*-
import unittest, doctest

from tagenwa.token import Token
from tagenwa.retokenizer.dictionary import DictionaryRetokenizer

class TestDictionaryRetokenizer(unittest.TestCase):
	
	def setUp(self):
		self.retokenizer = DictionaryRetokenizer()
		self.retokenizer.add(
			[u'hello'],
			[u'HELLO']
		)
		self.retokenizer.add(
			[u'good',u'morning'],
			[u'GOOD', u'MORNING']
		)
	
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
			self.assertEqual(e, self.retokenizer.retokenize(i))
	
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
			self.assertEqual(e, self.retokenizer.retokenize(i))



def suite():
	suite = unittest.TestSuite([
		unittest.TestLoader().loadTestsFromTestCase(TestDictionaryRetokenizer),
	])
	return suite

if __name__ == '__main__':
	unittest.main()