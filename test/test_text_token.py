# -*- coding: UTF-8 -*-
import unittest, doctest

from tagenwa.text.token import is_eol, is_hexadecimal, is_term, is_word

class TestToken(unittest.TestCase):	
	
	def test_util_doctest(self):
		import tagenwa.text.token
		failure_count, test_count = doctest.testmod(tagenwa.text.token)
		self.assertEqual(failure_count, 0, 'Testing doctest from tagenwa.text.token: %i failed out of %i' % (failure_count, test_count))
	
	
	def test_is_eol(self):
		testcases = [
			(u'abcde', False),
			(u'é', False),
			(u'あ', False),
			(u'a-b', False),
			(u'a_b', False),
			(u'ಠ_ಠ', False),
			(u'A1', False),
			(u'1', False),
			(u'①', False),
			(u'ⅱ', False),
			(u'四', False),
			(u'1.0', False),
			(u'1,000', False),
			(u'1,000.00', False),
			(u'0xABCDE', False),
			(u'。', False),
			(u'...', False),
			(u':', False),
			(u'', False),
			(u' ', False),
			(u'\t', False),
			(u'\n', True),
			(u'\r', True),
			(u'\r\n', True),
			(u'\n\n', True),
		]
		for i,e in testcases:
			self.assertEqual(e, is_eol(i), repr(i))
	
	
	def test_is_term(self):
		testcases = [
			# letters
			(u'abcde', True),
			(u'abc-de', True),
			(u'é', True),
			(u'あ', True),
			(u'a_b', True),
			(u'abc_x1', True),
			(u'ಠ_ಠ', True),
			# numbers
			(u'1', True),
			(u'①', True), # circled one
			(u'ⅱ', True), # Small Roman Numeral Two (U+2171)
			(u'四', True),
			(u'1.0', True),
			(u'1000', True),
			(u'1,000', True),
			(u'1,000.00', True),
			(u'0xABCDE', True),
			(u'0x1234', True),
			(u'0x12AB', True),
			(u'0xFFFF', True),
			# punctuations
			(u'_', False),
			(u'-', False),
			(u'=', False),
			(u'.', False),
			(u'。', False),
			(u'...', False),
			(u':', False),
			# empty
			(u'', False),
			# whitespace
			(u' ', False), # ascii space
			(u'　', False), # fullwidth space
			(u'\t', False),
			(u'\n', False),
			(u'\r\n', False),
		]
		for i,e in testcases:
			self.assertEqual(e, is_term(i), repr(i))
	
	
	def test_is_word(self):
		testcases = [
			# letters
			(u'abcde', True),
			(u'abc-de', True),
			(u'é', True),
			(u'あ', True),
			(u'a_b', False),
			(u'abc_x1', False),
			(u'ಠ_ಠ', False),
			# numbers
			(u'1', False),
			(u'①', False), # circled one (U+2460)
			(u'ⅱ', False), # Small Roman Numeral Two (U+2171)
			(u'四', True),
			(u'1.0', False),
			(u'1,000', False),
			(u'1,000.00', False),
			(u'0xABCDE', False),
			# punctuations
			(u'_', False),
			(u'-', False),
			(u'=', False),
			(u'.', False),
			(u'。', False),
			(u'...', False),
			(u':', False),
			# empty
			(u'', False),
			# whitespace
			(u' ', False), # ascii space
			(u'　', False), # fullwidth space
			(u'\t', False),
			(u'\n', False),
			(u'\r\n', False),
		]
		for i,e in testcases:
			self.assertEqual(e, is_word(i), repr(i))


def suite():
	suite = unittest.TestLoader().loadTestsFromTestCase(TestToken)
	return suite

if __name__ == '__main__':
	unittest.main()