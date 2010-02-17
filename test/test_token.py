# -*- coding: UTF-8 -*-
import unittest

from tagenwa.token import Token

class TestToken(unittest.TestCase):	
	
	def test_isalpha(self):
		testcases = [
			(u'abcde', True),
			(u'é', True),
			(u'あ', True),
			(u'A1', False),
			(u'1', False),
			(u'①', False),
			(u'ⅱ', False),
			(u'四', True),
			(u'1.0', False),
			(u'...', False),
			(u'a_b', False),
			(u'a-b', False),
			(u'a=b', False),
		]
		for i,e in testcases:
			self.assertEqual(e, Token(i).isalpha(), repr(i))
	
	def test_isalnum(self):
		testcases = [
			(u'abcde', True),
			(u'é', True),
			(u'あ', True),
			(u'A1', True),
			(u'1', True),
			(u'①', True),
			(u'ⅱ', True),
			(u'四', True),
			(u'1.0', False),
			(u'...', False),
			(u'a_b', False),
			(u'a-b', False),
			(u'a=b', False),
		]
		for i,e in testcases:
			self.assertEqual(e, Token(i).isalnum(), repr(i))
	
	def test_isnumeric(self):
		testcases = [
			(u'abcde', False),
			(u'a1', False),
			(u'1', True),
			(u'①', True),
			(u'ⅱ', True),
			(u'四', False),
			(u'1.0', False),
			(u'.', False),
			(u'é', False),
		]
		for i,e in testcases:
			self.assertEqual(e, Token(i).isnumeric(), repr(i))

	def test_isdigit(self):
		testcases = [
			(u'abcde', False),
			(u'a1', False),
			(u'1', True),
			(u'①', True),
			(u'ⅱ', False),
			(u'四', False),
			(u'1.0', False),
			(u'.', False),
			(u'é', False),
		]
		for i,e in testcases:
			self.assertEqual(e, Token(i).isdigit(), repr(i))

	def test_isdecimal(self):
		testcases = [
			(u'abcde', False),
			(u'a1', False),
			(u'1', True),
			(u'①', False),
			(u'ⅱ', False),
			(u'四', False),
			(u'1.0', False),
			(u'.', False),
			(u'é', False),
		]
		for i,e in testcases:
			self.assertEqual(e, Token(i).isdecimal(), repr(i))

	def test_ishexadecimal(self):
		testcases = [
			(u'abcde', False),
			(u'1', False),
			(u'四', False),
			(u'1.0', False),
			(u'.', False),
			(u'é', False),
			(u'0xabcde', True),
			(u'0xABCDE', True),
			(u'0x10abCDE', True),
			(u'0x1', True),
			(u'0x', False),
		]
		for i,e in testcases:
			self.assertEqual(e, Token(i).ishexadecimal(), repr(i))

	def test_isspace(self):
		testcases = [
			(u'abcde', False),
			(u'.', False),
			(u'é', False),
			(u'あ', False),
			(u'\t', True),
			(u'\r', True),
			(u'\n', True),
			(u'\r\n', True),
			(u'\n\n', True),
			(u' ', True), # ascii space
			(u'　', True), # fullwidth space
		]
		for i,e in testcases:
			self.assertEqual(e, Token(i).isspace(), repr(i))
	
	def test_iseol(self):
		testcases = [
			(u'abcde', False),
			(u'.', False),
			(u'é', False),
			(u'あ', False),
			(u'\t', False),
			(u'\r', True),
			(u'\n', True),
			(u'\r\n', True),
			(u'\n\n', True),
			(u' ', False), # ascii space
			(u'　', False), # fullwidth space
		]
		for i,e in testcases:
			self.assertEqual(e, Token(i).iseol(), repr(i))
	
	def test_isterm(self):
		testcases = [
			# letters
			(u'abcde', True),
			(u'abc-de', True),
			(u'é', True),
			(u'あ', True),
			# numbers
			(u'1', True),
			(u'①', False),
			(u'ⅱ', False),
			(u'四', True),
			# punctuations
			(u'a_b', True),
			(u'_', False),
			(u'-', False),
			(u'=', False),
			(u'.', False),
			(u':', False),
			# empty
			(u'', False),
			# whitespace
			(u' ', False),
			(u'\t', False),
			(u'\r\n', False),
			# look of disapproval
			(u'ಠ_ಠ', True),
		]
		for i,e in testcases:
			self.assertEqual(e, Token(i).isterm(), repr(i))
	
	def test_isword(self):
		testcases = [
			# letters
			(u'abcde', True),
			(u'abc-de', True),
			(u'é', True),
			(u'あ', True),
			# numbers
			(u'1', False),
			(u'①', False),
			(u'ⅱ', False),
			(u'四', True),
			# punctuations
			(u'a_b', False),
			(u'_', False),
			(u'-', False),
			(u'=', False),
			(u'.', False),
			(u':', False),
			# empty
			(u'', False),
			# whitespace
			(u' ', False),
			(u'\t', False),
			(u'\r\n', False),
			# look of disapproval
			(u'ಠ_ಠ', False),
		]
		for i,e in testcases:
			self.assertEqual(e, Token(i).isword(), repr(i))
	
	def test_haslatin(self):
		testcases = [
			# letters
			(u'abcde', True),
			(u'é', True),
			(u'a1', True),
			(u'a_b', True),
			(u'あ', False),
			# numbers
			(u'1', True),
			(u'①', False), # circled one
			(u'ⅱ', True), # Small Roman Numeral Two (U+2171)
			(u'四', False),
			# punctuations
			(u'_', True),
			(u'-', True),
			(u'=', True),
			(u'.', True),
			(u':', True),
			(u'。', False), # Japanese end of sentence marker
			# empty
			(u'', False),
			# whitespace
			(u' ', True), # ascii space
			(u'　', False), # fullwidth space
			(u'\t', True),
			(u'\r\n', True),
		]
		for i,e in testcases:
			self.assertEqual(e, Token(i).haslatin(), repr(i))


def suite():
	suite = unittest.TestLoader().loadTestsFromTestCase(TestToken)
	return suite

if __name__ == '__main__':
	unittest.main()