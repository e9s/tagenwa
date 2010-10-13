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
		# node structure is 'value', 'defined (bool)', 'children (dict)'
		self.root = [self.default, False, {}]
	
	
	def add(self, key, value):
		"""Add the given key-value pair to the trie.
		
		The key must be an iterable of hashable elements.
		"""
		node = self.root
		for k in key:
			node = node[2].setdefault(k, [self.default, False, {}])
		node[0], node[1] = value, True
	
	
	def remove(self, key):
		"""Remove the key from the trie.
		
		The key must be an iterable of hashable elements.
		"""
		try:
			node = self._get_node(key)
		except KeyError:
			raise KeyError('Key %s not found' % repr(key))
		if node[2]:
			# Perform a soft delete if there are children
			node[0], node[1] = self.default, False
		else:
			# Remove the node from its parent if it has no children
			parent_node = self._get_node(key[:-1])
			del parent_node[2][key[-1]]
			# TODO: Clean parents too if last children?
	
	
	def __contains__(self, key):
		"""Return True if the key is in the trie.
		
		The key must be an iterable of hashable elements.
		"""
		try:
			value = self._get_node(key)[1]
		except KeyError:
			value = False
		return value
	
	
	def get(self, key):
		"""Return the value of the given key or the trie's default value if the key is not found.
		
		The key must be an iterable of hashable elements.
		"""
		try:
			value = self._get_node(key)[0]
		except KeyError:
			value = self.default
		return value
	
	
	def find_prefix(self, key):
		"""Return the longuest prefix defined in the trie.
		
		The key must be an iterable of hashable elements.
		"""
		best_prefix = []
		path_prefix = []
		node = self.root
		for k in key:
			if k in node[2]:
				node = node[2][k]
				path_prefix.append(k)
				if node[1]:
					best_prefix = list(path_prefix)
			else:
				break
		return best_prefix
	
	
	def _get_node(self, key):
		"""Return the node linked to the key or raise KeyError if the key does not exist."""
		node = self.root
		for k in key:
			node = node[2][k]
		return node
	
	
	def __len__(self):
		"""Return the number of keys in the trie."""
		return sum(1 for k in self.keys())
	
	def keys(self, key=tuple()):
		"""Return the list of keys as tuples.
		
		The prefix of the list of keys can be specified with the `key` argument
		which must be an iterable of hashable elements.
		
		The keys are returned in a breadth-first order (keys with less elements are yielded first).
		The order within keys having the same number of elements is not defined.
		"""
		# Get the node defined by the prefix key
		try:
			node = self._get_node(key)
		except:
			return
		# Seed the stack with the root node
		# The stack is a list of tuples (full_key, node)
		stack= [(list(key),node)]
		# Go through the stack
		while len(stack) > 0:
			full_key, node = stack.pop()
			if node[1]:
				yield tuple(full_key)
			for k in node[2]:
				stack.append((full_key+[k],node[2][k]))

