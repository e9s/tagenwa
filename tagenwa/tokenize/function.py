# -*- coding: UTF-8 -*-


class FunctionRetokenizer(object):
	
	def __init__(self, functions):
		if callable(functions):
			functions = [functions]
		self.functions = functions
	
	def retokenize(self, tokens):
		"""Retokenize the tokens by applying each function."""
		for f in self.functions:
			tokens = f(tokens)
		return list(tokens)



class MapFilterRetokenizer(object):
	
	def __init__(self, functions):
		if callable(functions):
			functions = [functions]
		self.functions = functions
	
	def retokenize(self, tokens):
		"""Retokenize the tokens by applying each function and filtering out empty tokens."""
		stream = iter(tokens)
		for f in self.functions:
			stream = (f(token) for token in stream if token)
		return [token for token in stream if token]
