# -*- coding: UTF-8 -*-
import unittest, doctest

from tagenwa.tokenize.dictionary import DictionaryRetokenizer

class TestDictionaryRetokenizer(unittest.TestCase):
	
	def setUp(self):
		self.retokenizer1 = DictionaryRetokenizer()
		self.retokenizer2 = DictionaryRetokenizer(allow_overlap=True)
		
		for r in (self.retokenizer1, self.retokenizer2):
			r.add(
				[u'hello'],
				[u'HELLO']
			)
			r.add(
				[u'good', u'morning'],
				[u'GOOD', u'MORNING']
			)
			r.add(
				[u'morning', u'breakfast'],
				[u'MORNING', u'BREAKFAST']
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
			self.assertEqual(e, list(self.retokenizer1.retokenize(i)))
			self.assertEqual(e, list(self.retokenizer2.retokenize(i)))
	
	
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
			self.assertEqual(e, list(self.retokenizer1.retokenize(i)))
			self.assertEqual(e, list(self.retokenizer2.retokenize(i)))
	
	
	def test_overlap(self):
		testcases = [
			([u'abc', u'good',u'morning', u'breakfast'],[u'abc', u'GOOD',u'MORNING', u'breakfast']),
		]
		for i,e in testcases:
			self.assertEqual(e, list(self.retokenizer1.retokenize(i)))
		
		testcases = [
			([u'abc', u'good',u'morning', u'breakfast'],[u'abc', u'GOOD',u'MORNING', u'MORNING', u'BREAKFAST']),
		]
		for i,e in testcases:
			self.assertEqual(e, list(self.retokenizer2.retokenize(i)))



def suite():
	suite = unittest.TestSuite([
		unittest.TestLoader().loadTestsFromTestCase(TestDictionaryRetokenizer),
	])
	return suite

if __name__ == '__main__':
	unittest.main()