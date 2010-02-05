# -*- coding: UTF-8 -*-
import unittest

from tagenwa.uniscript import script, block
from unicodedata import normalize, name, category

class TestScript(unittest.TestCase):
	
	
	def test_block(self):
		testcases = [
			(u'a','Basic Latin'),
		]
		for i,e in testcases:
			self.assertEqual(block(i),e)
	
	def test_latin_letters(self):
		"""Test script: Latin"""
		testcases = u'aAåÅăĂąĄẬậɑⱭɐⱯæÆéÉèÈȄȅḿḾøØœŒÿŸ'
		for c in testcases:
			self.assertEqual(script(c), 'Latin')
	
	def test_cjk(self):
		"""Test script: Han"""
		testcases = u'気'
		for c in testcases:
			self.assertEqual(script(c), 'Han')
	
	def test_hiragana(self):
		"""Test script: Hiragana"""
		testcases = u'あいうえおはばぱをん'
		for c in testcases:
			self.assertEqual(script(c), 'Hiragana')
	
	def test_katakana(self):
		"""Test script: Katakana"""
		testcases = u'アイウエオハパバヲンー'
		for c in testcases:
			self.assertEqual(script(c, avoid_common=True), 'Katakana')


def suite():
	suite = unittest.TestLoader().loadTestsFromTestCase(TestScript)
	return suite

if __name__ == '__main__':
	unittest.main()