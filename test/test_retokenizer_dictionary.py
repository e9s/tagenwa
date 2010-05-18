# -*- coding: UTF-8 -*-
import unittest, doctest

from tagenwa.token import Token
from tagenwa.retokenizer.dictionary import DictionaryRetokenizer, MonolingualDictionaryRetokenizer

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



class TestMonolingualDictionaryRetokenizer(unittest.TestCase):
	
	def setUp(self):
		self.retokenizer = MonolingualDictionaryRetokenizer(lang=u'fr')
		self.retokenizer.add(
			[u'bonjour'],
			[Token(u'BONJOUR')]
		)
		self.retokenizer.add(
			[u'bonne',u'journée'],
			[Token(u'BONNE'), Token(u'JOURNEE')]
		)
	
	def test_simple(self):
		testcases = [
			([],[]),
			([(u'abc',u'fr')],[u'abc']),
			([(u'abc',u'en')],[u'abc']),
			([(u'bonjour', u'fr')],[u'BONJOUR']),
			([(u'bonjour', u'en')],[u'bonjour']),
			([(u'abc',u'fr'), (u'bonjour',u'fr')],[u'abc', u'BONJOUR']),
			([(u'abc',u'en'), (u'bonjour',u'fr')],[u'abc', u'BONJOUR']),
			([(u'abc',u'fr'), (u'bonjour',u'en')],[u'abc', u'bonjour']),
			([(u'abc',u'en'), (u'bonjour',u'en')],[u'abc', u'bonjour']),
			([(u'bonjour',u'fr'), (u'xyz',u'fr')],[u'BONJOUR', u'xyz']),
			([(u'bonjour',u'fr'), (u'xyz',u'en')],[u'BONJOUR', u'xyz']),
			([(u'bonjour',u'en'), (u'xyz',u'fr')],[u'bonjour', u'xyz']),
			([(u'bonjour',u'en'), (u'xyz',u'en')],[u'bonjour', u'xyz']),
			([(u'abc',u'fr'), (u'bonjour',u'fr'), (u'xyz',u'fr')],[u'abc', u'BONJOUR', u'xyz']),
			([(u'abc',u'en'), (u'bonjour',u'fr'), (u'xyz',u'en')],[u'abc', u'BONJOUR', u'xyz']),
			([(u'abc',u'en'), (u'bonjour',u'en'), (u'xyz',u'en')],[u'abc', u'bonjour', u'xyz']),
			([(u'abc',u'fr'), (u'bonjour',u'en'), (u'xyz',u'fr')],[u'abc', u'bonjour', u'xyz']),
		]
		for i,e in testcases:
			self.assertEqual(e, [token.text for token in self.retokenizer.retokenize([Token(t).set(u'lang',lang) for t,lang in i])])
	
	def test_compound(self):
		testcases = [
			([],[]),
			([(u'abc',u'fr')],[u'abc']),
			([(u'abc',u'en')],[u'abc']),
			([(u'bonne',u'fr'), (u'journée',u'fr')],[u'BONNE',u'JOURNEE']),
			([(u'bonne',u'en'), (u'journée',u'fr')],[u'bonne',u'journée']),
			([(u'bonne',u'fr'), (u'journée',u'en')],[u'bonne',u'journée']),
			([(u'bonne',u'en'), (u'journée',u'en')],[u'bonne',u'journée']),
			([(u'abc',u'fr'), (u'bonne',u'fr'), (u'journée',u'fr')],[u'abc', u'BONNE',u'JOURNEE']),
			([(u'abc',u'en'), (u'bonne',u'fr'), (u'journée',u'fr')],[u'abc', u'BONNE',u'JOURNEE']),
			([(u'abc',u'en'), (u'bonne',u'en'), (u'journée',u'en')],[u'abc', u'bonne',u'journée']),
			([(u'abc',u'fr'), (u'bonne',u'en'), (u'journée',u'en')],[u'abc', u'bonne',u'journée']),
			([(u'abc',u'en'), (u'bonne',u'fr'), (u'journée',u'en')],[u'abc', u'bonne',u'journée']),
			([(u'abc',u'fr'), (u'bonne',u'fr'), (u'journée',u'en')],[u'abc', u'bonne',u'journée']),
			([(u'abc',u'en'), (u'bonne',u'en'), (u'journée',u'fr')],[u'abc', u'bonne',u'journée']),
			([(u'abc',u'fr'), (u'bonne',u'en'), (u'journée',u'fr')],[u'abc', u'bonne',u'journée']),
			([(u'bonne',u'fr'), (u'journée',u'fr'), (u'xyz', u'fr')],[u'BONNE',u'JOURNEE', u'xyz']),
			([(u'bonne',u'fr'), (u'journée',u'fr'), (u'xyz', u'en')],[u'BONNE',u'JOURNEE', u'xyz']),
			([(u'bonne',u'en'), (u'journée',u'en'), (u'xyz', u'fr')],[u'bonne',u'journée', u'xyz']),
			([(u'bonne',u'en'), (u'journée',u'en'), (u'xyz', u'en')],[u'bonne',u'journée', u'xyz']),
			([(u'bonne',u'fr'), (u'journée',u'en'), (u'xyz', u'fr')],[u'bonne',u'journée', u'xyz']),
			([(u'bonne',u'fr'), (u'journée',u'en'), (u'xyz', u'en')],[u'bonne',u'journée', u'xyz']),
			([(u'bonne',u'en'), (u'journée',u'fr'), (u'xyz', u'fr')],[u'bonne',u'journée', u'xyz']),
			([(u'bonne',u'en'), (u'journée',u'fr'), (u'xyz', u'en')],[u'bonne',u'journée', u'xyz']),
		]
		for i,e in testcases:
			self.assertEqual(e, [token.text for token in self.retokenizer.retokenize([Token(t).set(u'lang',lang) for t,lang in i])])


def suite():
	suite = unittest.TestSuite([
		unittest.TestLoader().loadTestsFromTestCase(TestDictionaryRetokenizer),
		unittest.TestLoader().loadTestsFromTestCase(TestMonolingualDictionaryRetokenizer),
	])
	return suite

if __name__ == '__main__':
	unittest.main()