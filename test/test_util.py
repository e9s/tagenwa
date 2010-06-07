# -*- coding: UTF-8 -*-
import unittest, doctest

from tagenwa.util import sliding_tuples, copycase, sub


class TestUtil(unittest.TestCase):
	
	def test_util_doctest(self):
		import tagenwa.util
		failure_count, test_count = doctest.testmod(tagenwa.util)
		self.assertEqual(failure_count, 0, 'Testing doctest from tagenwa.util: %i failed out of %i' % (failure_count, test_count))

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
	
	def test_copycase(self):
		testcases = [
			# empty
			(u'', u'', u''),
			(u'', u'x', u''),
			(u'', u'X', u''),
			# single
			(u'a', u'x', u'a'),
			(u'a', u'X', u'A'),
			(u'a', u'xxx', u'a'),
			(u'a', u'XXX', u'A'),
			(u'a', u'Xxx', u'A'),
			# shorter
			(u'aa', u'xxx', u'aa'),
			(u'aa', u'Xxx', u'Aa'),
			(u'aa', u'xXx', u'aA'),
			(u'aa', u'XXx', u'AA'),
			(u'aa', u'xxX', u'aa'),
			(u'aa', u'XxX', u'Aa'),
			(u'aa', u'xXX', u'aA'),
			(u'aa', u'XXX', u'AA'),
			# equal length
			(u'aaa', u'xxx', u'aaa'),
			(u'aaa', u'Xxx', u'Aaa'),
			(u'aaa', u'xXx', u'aAa'),
			(u'aaa', u'XXx', u'AAa'),
			(u'aaa', u'xxX', u'aaA'),
			(u'aaa', u'XxX', u'AaA'),
			(u'aaa', u'xXX', u'aAA'),
			(u'aaa', u'XXX', u'AAA'),
		]
		for (i1,i2,e) in testcases:
			self.assertEqual(e, copycase(i1,i2), (i1,i2,e))
	
	def test_sub_string(self):
		testcases = [
			# simple
			('abcde',set(['bc']),['a','BC','X','d','e']),
			('abcde',set(['bc','xx']),['a','BC','X','d','e']),
			# first position
			('abcde',set(['ab','xx']),['AB','X','c','d','e']),
			# last position
			('abcde',set(['de','xx']),['a','b','c','DE','X']),
			# overlap
			('abcde',set(['de','abcd']),['ABCD','X','e']),
			# include
			('abcde',set(['abcd','bc']),['ABCD','X','e']),
			('abcde',set(['abcd','ab']),['ABCD','X','e']),
			('abcde',set(['abcd','cd']),['ABCD','X','e']),
		]
		replace = lambda x:[''.join(x).upper(),'X']
		key = lambda x:''.join(x) if None not in x else None
		for i,s,e in testcases:
			match = lambda x:key(x) in s
			maxlength = max(len(t) for t in s)
			self.assertEqual(e, list(sub(i, match, replace, maxlength)))


def suite():
	suite = unittest.TestLoader().loadTestsFromTestCase(TestUtil)
	return suite

if __name__ == '__main__':
	unittest.main()