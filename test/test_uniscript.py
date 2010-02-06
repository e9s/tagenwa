# -*- coding: UTF-8 -*-
import unittest

from tagenwa.uniscript import script, block


class TestScript(unittest.TestCase):
	
	
	def test_block(self):
		testcases = [
			(u'a','Basic Latin'),
			(u'A','Basic Latin'),
			(u'+','Basic Latin'),
			(u'$','Basic Latin'),
			(u'é','Latin-1 Supplement'),
			(u'è','Latin-1 Supplement'),
		]
		for i,e in testcases:
			self.assertEqual(block(i),e)
	
	def test_latin_letters(self):
		"""Test script: Latin"""
		testcases = u'aAåÅăĂąĄẬậɑⱭɐⱯæÆéÉèÈȄȅḿḾøØœŒÿŸ'
		for c in testcases:
			self.assertEqual(script(c, avoid_common=True), 'Latin')
			self.assertEqual(script(c, avoid_common=False), 'Latin')
	
	def test_cjk(self):
		"""Test script: Han"""
		testcases = u'気'
		for c in testcases:
			self.assertEqual(script(c, avoid_common=True), 'Han')
			self.assertEqual(script(c, avoid_common=False), 'Han')
	
	def test_hiragana(self):
		"""Test script: Hiragana"""
		testcases = u'あいうえおはばぱをん'
		for c in testcases:
			self.assertEqual(script(c, avoid_common=True), 'Hiragana')
			self.assertEqual(script(c, avoid_common=False), 'Hiragana')
	
	def test_katakana(self):
		"""Test script: Katakana"""
		testcases1 = u'アイウエオハパバヲン'
		for c in testcases1:
			self.assertEqual(script(c, avoid_common=False), 'Katakana')
		testcases2 = u'ー'
		for c in testcases1+testcases2:
			self.assertEqual(script(c, avoid_common=True), 'Katakana')


def suite():
	suite = unittest.TestLoader().loadTestsFromTestCase(TestScript)
	return suite

if __name__ == '__main__':
	unittest.main()