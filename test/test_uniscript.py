# -*- coding: UTF-8 -*-
import unittest

from tagenwa.uniscript import script

class TestScript(unittest.TestCase):
	
	def test_latin_letters(self):
		"""Test script: latin letters"""
		testcases = u'aAåÅăĂąĄẬậɑⱭɐⱯæÆéÉèÈȄȅḿḾøØœŒÿŸ'
		for c in testcases:
			self.assertEqual(script(c), u'latin')
	
	def test_cjk(self):
		"""Test script: CJK"""
		testcases = u'気'
		for c in testcases:
			self.assertEqual(script(c), u'cjk')
	
	def test_hiragana(self):
		"""Test script: hiragana"""
		testcases = u'あいうえおはばぱをん'
		for c in testcases:
			self.assertEqual(script(c), u'hiragana')
	
	def test_katakana(self):
		"""Test script: katakana"""
		testcases = u'アイウエオハパバヲンー'
		for c in testcases:
			self.assertEqual(script(c), u'katakana')


def suite():
	suite = unittest.TestLoader().loadTestsFromTestCase(TestScript)
	return suite

if __name__ == '__main__':
	unittest.main()