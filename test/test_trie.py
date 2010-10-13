# -*- coding: UTF-8 -*-
import unittest

from tagenwa.util.trie import Trie

class TestTrie(unittest.TestCase):	
	
	def setUp(self):
		trie = Trie()
		
		# Add some value
		trie.add('abc', 3)
		trie.add('ab', 2)
		trie.add('abcd', 4)
		trie.add('abcdef', 5)
		trie.add('xyz', 999)
		
		self.trie = trie
	
	
	def test_get(self):
		trie = self.trie
		
		# test existing key
		self.assertEqual(trie.get('ab'), 2)
		self.assertEqual(trie.get('abc'), 3)
		self.assertEqual(trie.get('abcd'), 4)
		self.assertEqual(trie.get('abcdef'), 5)
		self.assertEqual(trie.get('xyz'), 999)
		
		# test missing key
		self.assertEqual(trie.get(''), None)
		self.assertEqual(trie.get('a'), None)
		self.assertEqual(trie.get('abx'), None)
		self.assertEqual(trie.get('abcde'), None)
		self.assertEqual(trie.get('abcdx'), None)
		self.assertEqual(trie.get('abcdefg'), None)
	
	
	def test_in(self):
		trie = self.trie
		
		# test existing key
		self.assertTrue('ab' in trie)
		self.assertTrue('abc' in trie)
		self.assertTrue('abcd' in trie)
		self.assertTrue('abcdef' in trie)
		self.assertTrue('xyz' in trie)
		
		# test missing key
		self.assertFalse('' in trie)
		self.assertFalse('a' in trie)
		self.assertFalse('abx' in trie)
		self.assertFalse('abcde' in trie)
		self.assertFalse('abcdx' in trie)
		self.assertFalse('abcdefgh' in trie)
	
	
	def test_remove(self):
		trie = self.trie
		
		trie.remove('abc')
		
		# test removed key
		self.assertEqual(trie.get('abc'), None)
		
		# test existing key
		self.assertEqual(trie.get('ab'), 2)
		self.assertEqual(trie.get('abcd'), 4)
		self.assertEqual(trie.get('abcdef'), 5)
		self.assertEqual(trie.get('xyz'), 999)
		
		# test missing key
		self.assertEqual(trie.get(''), None)
		self.assertEqual(trie.get('a'), None)
		self.assertEqual(trie.get('abx'), None)
		self.assertEqual(trie.get('abcde'), None)
		self.assertEqual(trie.get('abcdx'), None)
		self.assertEqual(trie.get('abcdefg'), None)
		
		# test all keys
		keys = list(trie.keys())
		self.assertEqual(set(keys), set([tuple('ab'),tuple('abcd'),tuple('abcdef'),tuple('xyz')]))
	
	
	def test_remove_leaf(self):
		trie = self.trie
		
		trie.remove('abcdef')
		
		# test removed key
		self.assertEqual(trie.get('abcdef'), None)
		
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
		self.assertEqual(trie.get('abcdx'), None)
		self.assertEqual(trie.get('abcdefg'), None)
		
		# test all keys
		keys = list(trie.keys())
		self.assertEqual(set(keys), set([tuple('ab'),tuple('abc'),tuple('abcd'),tuple('xyz')]))
	
	
	def test_find_prefix(self):
		trie = self.trie
		
		# test existing key
		self.assertEqual(trie.find_prefix('ab'), list('ab'))
		self.assertEqual(trie.find_prefix('abc'), list('abc'))
		self.assertEqual(trie.find_prefix('abcd'), list('abcd'))
		self.assertEqual(trie.find_prefix('abcdef'), list('abcdef'))
		self.assertEqual(trie.find_prefix('xyz'), list('xyz'))
		
		# test missing key
		self.assertEqual(trie.find_prefix(''), [])
		self.assertEqual(trie.find_prefix('a'), [])
		self.assertEqual(trie.find_prefix('abx'), list('ab'))
		self.assertEqual(trie.find_prefix('abcde'), list('abcd'))
		self.assertEqual(trie.find_prefix('abcdx'), list('abcd'))
		self.assertEqual(trie.find_prefix('abcdefgh'), list('abcdef'))
	
	
	def test_keys(self):
		trie = self.trie
		
		keys = list(trie.keys())
		self.assertEqual(len(trie), 5)
		self.assertEqual(len(keys), 5)
		self.assertEqual(set(keys), set([tuple('ab'),tuple('abc'),tuple('abcd'),tuple('abcdef'),tuple('xyz')]))
		
		# keys starting with a specified prefix
		keys = list(trie.keys('abc'))
		self.assertEqual(len(keys), 3)
		self.assertEqual(set(keys), set([tuple('abc'),tuple('abcd'),tuple('abcdef')]))
		
		# prefix not existing
		keys = list(trie.keys('pqr'))
		self.assertEqual(len(keys), 0)
		
		


def suite():
	suite = unittest.TestLoader().loadTestsFromTestCase(TestTrie)
	return suite

if __name__ == '__main__':
	unittest.main()