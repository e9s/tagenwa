# -*- coding: UTF-8 -*-
import unittest, doctest

from tagenwa.utils.iterators import sliding_tuples, counts


class TestUtils(unittest.TestCase):
	
	def test_util_doctest(self):
		import tagenwa.utils.iterators
		failure_count, test_count = doctest.testmod(tagenwa.utils.iterators)
		self.assertEqual(failure_count, 0, 'Testing doctest from tagenwa.utils.iterators: %i failed out of %i' % (failure_count, test_count))

	def test_sliding_tuples(self):
		testcases = [
			(
				('abc', 1),
				[('a',), ('b',),('c',)]
			),
			(
				('abc', 1, None, False, False),
				[('a',), ('b',),('c',)]
			),
			(
				('abc', 2),
				[(None,'a'),('a','b'),('b','c'),('c',None)]
			),
			(
				('abc', 2, None, True, True),
				[(None,'a'),('a','b'),('b','c'),('c',None)]
			),
			(
				('abc', 2, None, False, False),
				[('a','b'),('b','c')]
			),
			(
				('abc', 2, None, True, False),
				[(None,'a'),('a','b'),('b','c')]
			),
			(
				('abc', 2, None, False, True),
				[('a','b'),('b','c'),('c',None)]
			),
			(
				('abc', 3, None, False, True),
				[('a','b','c'), ('b','c',None),('c',None,None)]
			),
			(
				('abc', 3, None, True),
				[(None,None,'a'), (None,'a','b'), ('a','b','c'), ('b','c',None), ('c',None,None)]
			),
			(
				('abc', 4, None, False, True),
				[('a','b','c',None), ('b','c',None,None),('c',None,None,None)]
			),
			(
				('abc', 4, None, True, True),
				[(None,None,None,'a'), (None,None,'a','b'), (None,'a','b','c'), ('a','b','c',None), ('b','c',None,None),('c',None,None,None)]
			),
			# test fillvalue
			(
				('abc', 2, 'x'),
				[('x','a'), ('a','b'), ('b','c'),('c','x')]
			),
			# test with an iterator
			(
				(xrange(4), 2),
				[(None,0),(0,1),(1,2),(2,3),(3,None)]
			),
		]
		for (i,e) in testcases:
			self.assertEqual(e, list(sliding_tuples(*i)))



def suite():
	suite = unittest.TestLoader().loadTestsFromTestCase(TestUtils)
	return suite

if __name__ == '__main__':
	unittest.main()