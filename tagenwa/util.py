# -*- coding: UTF-8 -*-
"""
Useful functions for tokenization

"""

from itertools import tee, chain, izip, izip_longest
# INFO: izip_longest is new in Python 2.6


def sliding_tuples(iterable, length, fillvalue=None, filllead=True, filltail=True):
	"""Generate an iterable of tuples of consecutive items from the iterable.
	
	Simple usage:
	>>> list(sliding_tuples(xrange(4), 3))
	[(None, None, 0), (None, 0, 1), (0, 1, 2), (1, 2, 3), (2, 3, None), (3, None, None)]
	
	Avoiding tuples partially outside of the iterable:
	>>> list(sliding_tuples(xrange(4), 3, filllead=False, filltail=False))
	[(0, 1, 2), (1, 2, 3)]
	
	:param iterable: an iterable
	:param length: the length of the tuples to return
	:type length: int
	:param fillvalue: the value to used for filling when the tuple is partially outside of the iterable (default None)
	:param filllead: True if partial tuples should be returned at the beginning (default True)
	:type filllead: bool
	:param filltail: True if partial tuples should be returned at the end (default True)
	:type filltail: bool
	:return: iterable of tuples
	:rtype: generator
	"""
	
	# fill lead if needed
	if filllead:
		iterable = chain([fillvalue]*(length-1), iterable)
	
	# make a list of n iterables
	# and initialize each iterable by shifting it according to his index
	iterables = tee(iterable, length)
	for i in xrange(1,length):
		for j in xrange(i):
			try:
				iterables[i].next()
			except StopIteration as e:
				# leave iterable closed if shorter than 'length'
				# (izip_longuest will take care of it)
				pass
	
	# fill tail if needed
	if filltail:
		zipped = izip_longest(*iterables, fillvalue=fillvalue)
	else:
		zipped = izip(*iterables)
	
	# yield the tuples
	for tu in zipped:
			yield tu
