# -*- coding: UTF-8 -*-
"""
Trie

"""
__license__ = "MIT"


class Trie(object):
	"""Trie"""
	
	def __init__(self, default=None):
		"""Create a new trie.
		
		A default value can be specified for non-existing keys.  By default,
		the default value is None.
		"""
		self.default = default
		self.root = [self.default, False, {}]
	
	
	def add(self, key, value):
		"""Add the given key-value pair to the trie."""
		node = self.root
		for k in key:
			node = node[2].setdefault(k, [self.default, False, {}])
		node[0], node[1] = value, True
	
	
	def get(self, key):
		"""Return the value of the given key or the trie's default value if the key is not found.
		"""
		try:
			node = self._get_node(key)
		except KeyError:
			return self.default
		return node[0]
	
	
	def find_prefix(self, key):
		"""Find the longuest prefix and return the prefix and its value.
		
		Return the tuple (prefix, value).
		"""
		node = self.root
		prefix = []
		for k in key:
			try:
				node = node[2][k]
				prefix.append(k)
			except KeyError:
				break
		return (prefix, node[0])
	
	
	def _get_node(self, key):
		"""Return the node linked to the key or raise KeyError if the key does not exist."""
		node = self.root
		for k in key:
			node = node[2][k]
		return node
	
	
	def keys(self, key=tuple()):
		"""Return the list of keys as tuples.
		
		The prefix of the list of keys can be specified with the `key` argument.
		"""
		# get the prefix key
		try:
			node = self._get_node(key)
		except:
			return
		# set the stack with the root note as seed
		stack= [(tuple(key),node)]
		# go through the stack
		while len(stack) > 0:
			key, node = stack.pop()
			if node[1]:
				yield key
			for k in node[2]:
				prefix = list(key)
				stack.append((tuple(prefix+[k]),node[2][k]))
		
