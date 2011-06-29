# -*- coding: UTF-8 -*-
"""
Useful functions for handling iterables

"""
from itertools import tee, chain, izip, izip_longest
# INFO: izip_longest is new in Python 2.6
from collections import defaultdict


def sliding_tuples(iterable, length, fill_value=None, fill_lead=True, fill_tail=True):
	"""Generate an iterable of tuples of consecutive items from the iterable.
	
	Simple usage:
	>>> list(sliding_tuples(xrange(4), 3))
	[(None, None, 0), (None, 0, 1), (0, 1, 2), (1, 2, 3), (2, 3, None), (3, None, None)]
	
	Avoiding tuples partially outside of the iterable:
	>>> list(sliding_tuples(xrange(4), 3, fill_lead=False, fill_tail=False))
	[(0, 1, 2), (1, 2, 3)]
	
	:param iterable: an iterable
	:param length: the length of the tuples to return
	:type length: int
	:param fill_value: the value to used for filling when the tuple is partially outside of the iterable (default is None)
	:param fill_lead: True if partial tuples should be returned at the beginning (default is True)
	:type fill_lead: bool
	:param fill_tail: True if partial tuples should be returned at the end (default is True)
	:type fill_tail: bool
	:return: iterable of tuples
	:rtype: iterator
	"""
	
	# fill lead if needed
	if fill_lead:
		iterable = chain([fill_value]*(length-1), iterable)
	
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
	if fill_tail:
		zipped = izip_longest(*iterables, fillvalue=fill_value)
	else:
		zipped = izip(*iterables)
	
	# yield the tuples
	for tu in zipped:
		yield tu


def counts(iterable):
	"""Return a dictionary of occurences."""
	d = defaultdict(int)
	for i in iterable:
		d[i] += 1
	return dict(d)


def merge_tagged(iterable, merge_tokens=None):
	"""Return an iterable of tagged tokens where the consecutive tokens having the same tag
	in the given iterable have been merged."""
	# Initialize the iteration
	iterator = iter(iterable)
	try:
		token, tag0 = iterator.next()
		buffer = [token]
	except StopIteration:
		# Re-raise the StopIteration in case of empty iterator
		raise
	
	if merge_tokens is None:
		merge_tokens = lambda x:x
	
	# Merge consecutive tokens having the same tag
	merged_tagged = []
	for token, tag in iterator:
		if tag != tag0:
			yield (merge_tokens(buffer), tag0)
			buffer = [token]
			tag0 = tag
		else:
			buffer.append(token)
	yield (merge_tokens(buffer), tag0)
