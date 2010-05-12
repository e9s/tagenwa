# -*- coding: UTF-8 -*-
"""
Useful functions for tokenization

"""

from itertools import tee, chain, izip, izip_longest
# INFO: izip_longest is new in Python 2.6
from collections import defaultdict
from threading import Lock

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


def group_count(iterable):
	"""Return a dictionary of occurences."""
	d = defaultdict(int)
	for i in iterable:
		d[i] += 1
	return dict(d)


def copycase(text, reference):
	"""Return a copy of `text` with a case similar to `reference`.
	
	If the reference text is all lower case, all upper case or in title case,
	the returned value will be in all lower case, all upper case or in title case
	respectively.
	
	If the original text is shorter or has the same length as the reference text,
	then the casing of the reference text is applied to the original text character by character.
	
	If none of these previous conditions are met, the original text is returned
	as is.
	
	Lower, upper or title case:
	>>> copycase(u'aBc', u'xxxxx')
	u'abc'
	>>> copycase(u'aBc', u'XXXXX')
	u'ABC'
	>>> copycase(u'aBc', u'Xxxxx')
	u'Abc'
	
	Same length:
	>>> copycase(u'aBc', u'xxX')
	u'abC'
	
	:param text: the text for which the case should be modified
	:type text: unicode
	:param reference: a text to use as reference for the choice of the case
	:type reference: unicode
	:return: a copy of the text with a case similar to `reference`
	:rtype: unicode
	"""
	if reference.islower():
		return text.lower()
	elif reference.isupper():
		return text.upper()
	elif reference.istitle():
		return text.title()
	elif len(text) <= len(reference):
		return u''.join(
			c.lower() if c0.islower() else
			c.upper() if c0.isupper() else
			c
			for c,c0 in zip(text,reference)
		)
	# by default, return text
	return text


def sub(iterable, match, replace, maxlength):
	"""
	Substitute continuous elements in the iterable.
	
	The `match` function returns a boolean indicating if the continuous elements
	must be replaced.
	The `replace` function returns an iterable of elements to use as replacement.
	
	>>> dictionary = set([('b','c'),('b','c','f')])
	>>> match = lambda x:x in dictionary
	>>> # replace() joins characters together and converts them to upper case
	>>> replace = lambda x:[''.join(x).upper()]
	>>> maxlength = max(len(t) for t in dictionary)
	>>> list(sub('abcde', match, replace, maxlength))
	['a', 'BC', 'd', 'e']
	
	The `sub` function iterates several times over the iterable,
	each time with a smaller sliding tuple length,
	to generate all the possible tuples of continuous elements.
	The time complexity of the `sub` function is therefore `O(t*n)`
	where `t` is the length of the iterable
	and `n` is the maximum length of the sliding windows
	as specified by the `maxlength` argument.
	
	:param iterable: iterable with elements to substitute
	:type iterable: iterable
	:param match: function returning True if the tuple of consecutive elements should be replaced
	:type match: function
	:param replace: function returning an iterable of replacement elements
	:type replace: function
	:param maxlength: maximum length of consecutive elements to check 
	:type maxlength: int
	:return: iterable of elements
	:rtype: iterable
	"""
	tuples = sliding_tuples(iterable, maxlength, filllead=False, filltail=True)
	for tu0 in tuples:
		replacing = False
		# check each sub-tuple
		for length in xrange(maxlength, 0, -1):
			tu = tuple(tu0[:length])
			if match(tu):
				replacing = True
				# yield the replacing elements
				for r in replace(tu):
					yield r
				# move forward the sliding tuples iterable
				try:
					for j in xrange(length-1):
						tuples.next()
				except:
					continue
		# yield the original element if no replacement
		if not replacing:
			yield tu0[0]
	#TODO sub in end of iterable
	return


def memoize(size=512):
	"""Memoizing decorator with LFU cache.
	
	The memoize decorator should be used like this:
	>>> @memoize(size=127)
	... def f(arg):
	...     # code here
	...     pass
	
	The `memoize` decorator is written to be thread-safe but the decorator
	does not render the memoized function thread-safe.
	
	:param size: maximum size of the LFU cache
	:type size: int
	"""
	def decorator(f):
		cache = {}
		lfukeys = []
		lock = Lock()
		def wrapper(*args,**kwargs):
			key = (args,frozenset(kwargs.items()))
			# get the value (and remove the key from the LFU list if found)
			lock.acquire()
			if key in cache:
				value = cache[key]
				try:
					lfukeys.remove(key)
				except ValueError:
					# this should never happen
					pass
				lock.release()
			else:
				lock.release()
				# calculate the value outside of the critical section
				# as the function execution may be long so we could want to multi-thread it
				value = f(*args,**kwargs)
				lock.acquire()
				cache[key] = value
				lock.release()
			# add the key to the top of the LFU list
			lock.acquire()
			lfukeys.append(key)
			# delete the least frequently used item
			if len(lfukeys) > size:
				del cache[lfukeys.pop(0)]
			lock.release()
			return value
		# store the original function
		wrapper._original = f
		# copy the magic values of the original function
		wrapper.__doc__ = f.__doc__
		wrapper.__name__ = f.__name__
		wrapper.__module__ = f.__module__
		return wrapper
	return decorator
	