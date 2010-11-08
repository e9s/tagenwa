# -*- coding: UTF-8 -*-
from tagenwa.util.tools import sliding_tuples
from tagenwa.token import Token


class NumberRetokenizer(object):
	
	def __init__(self, token_key=None, token_value=None):
		"""Create a new NumberRetokenizer.
		
		The NumberRetokenizer merges the symbols '.' or ',' with the previous and
		next tokens if they are both decimal tokens.  It also merges two consecutive
		decimal tokens.
		
		This retokenizer should be run before removing the whitespace tokens.
		
		Optionally, the retokenizer can also set a token property `token_key`
		with value `token_value` to the recognized decimal tokens
		if the arguments `token_key` is not None.
		
		:param token_key: key of the property to be set for decimal tokens (optional)
		:type token_key: hashable
		:param token_value: value of the property to be set for decimal tokens
		"""
		self.token_key = token_key
		self.token_value = token_value
	
	
	def retokenize(self, tokens):
		prev_token = None
		is_prev_null = True
		filler = object()
		
		token_tuples = sliding_tuples(tokens, 2, fill_value = filler, fill_lead=False, fill_tail=True)
		for t0, t1 in token_tuples:
			# Continue until a number token is found
			if is_prev_null:
				if t0.isdecimal():
					if self.token_key is not None:
						t0.set(self.token_key, self.token_value)
					prev_token = t0
					is_prev_null = False
				else:
					yield t0
				continue
			
			if (
					t0.isdecimal()
					or (t0.text in (u'.', u',') and t1 is not filler and t1.isdecimal())
				):
				# Merge the token t0 with the previous number token
				prev_token = Token(prev_token.text + t0.text)
				if self.token_key is not None:
					prev_token.set(self.token_key, self.token_value)
			else:
				# Don't merge the tokens and yield the previous token
				yield prev_token
				yield t0
				prev_token = None
				is_prev_null = True
		
		# Yield the last element
		if not is_prev_null:
			yield prev_token
		return
	
