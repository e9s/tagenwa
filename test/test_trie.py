# -*- coding: UTF-8 -*-
import unittest

from tagenwa.trie import Trie

class TestTrie(unittest.TestCase):	
	
	def setUp(self):
		trie = Trie()
		
		# Add some value
		trie.add('abc', 3)
		trie.add('ab', 2)
		trie.add('abcd', 4)
		trie.add('xyz', 999)
		
		self.trie = trie
	
	
	def test_get(self):
		trie = self.trie
		
		# test existing key
		self.assertEqual(trie.get('ab'), 2)
		self.assertEqual(trie.get('abc'), 3)
		self.assertEqual(trie.get('abcd'), 4)
		self.assertEqual(trie.get('xyz'), 999)
		
		# test missing key
		self.assertEqual(trie.get(''), None)
		self.assertEqual(trie.get('a'), None)
		self.assertEqual(trie.get('abx'), None)
		self.assertEqual(trie.get('abcde'), None)
	
	
	def test_remove(self):
		trie = self.trie
		
		trie.remove('abc')
		# test existing key
		self.assertEqual(trie.get('ab'), 2)
		self.assertEqual(trie.get('abc'), None)
		self.assertEqual(trie.get('abcd'), 4)
		self.assertEqual(trie.get('xyz'), 999)
		
		# test missing key
		self.assertEqual(trie.get(''), None)
		self.assertEqual(trie.get('a'), None)
		self.assertEqual(trie.get('abx'), None)
		self.assertEqual(trie.get('abcde'), None)
	
	
	def test_find_prefix(self):
		trie = self.trie
		
		# test existing key
		self.assertEqual(trie.find_prefix('ab'), (list('ab'),2))
		self.assertEqual(trie.find_prefix('abc'), (list('abc'),3))
		self.assertEqual(trie.find_prefix('abcd'), (list('abcd'),4))
		self.assertEqual(trie.find_prefix('xyz'), (list('xyz'),999))
		
		# test missing key
		self.assertEqual(trie.find_prefix(''), (list(''),None))
		self.assertEqual(trie.find_prefix('a'), (list('a'),None))
		self.assertEqual(trie.find_prefix('abx'), (list('ab'),2))
		self.assertEqual(trie.find_prefix('abcde'), (list('abcd'),4))
	
	def test_keys(self):
		trie = self.trie
		
		keys = list(trie.keys())
		self.assertEqual(len(keys), 4)
		self.assertEqual(set(keys), set([tuple('ab'),tuple('abc'),tuple('abcd'),tuple('xyz')]))
		
		# keys starting with a specified prefix
		keys = list(trie.keys('abc'))
		self.assertEqual(len(keys), 2)
		self.assertEqual(set(keys), set([tuple('abc'),tuple('abcd')]))
		
		# prefix not existing
		keys = list(trie.keys('pqr'))
		self.assertEqual(len(keys), 0)
		
		


def suite():
	suite = unittest.TestLoader().loadTestsFromTestCase(TestTrie)
	return suite

if __name__ == '__main__':
	unittest.main()