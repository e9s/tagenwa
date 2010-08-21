# -*- coding: UTF-8 -*-
import unittest, doctest

from tagenwa.uniscript import script, block


class TestScript(unittest.TestCase):
	
	def test_uniscript_doctest(self):
		import tagenwa.uniscript
		failure_count, test_count = doctest.testmod(tagenwa.uniscript)
		self.assertEqual(failure_count, 0, 'Testing doctest from tagenwa.uniscript: %i failed out of %i' % (failure_count, test_count))
	
	
	def test_block(self):
		testcases = [
			(u'a','Basic Latin'),
			(u'A','Basic Latin'),
			(u'+','Basic Latin'),
			(u'$','Basic Latin'),
			(u'é','Latin-1 Supplement'),
			(u'è','Latin-1 Supplement'),
			(u'ó','Latin-1 Supplement'),
			(u'д','Cyrillic'),
			(u'ค','Thai'),
			(u'氣','CJK Unified Ideographs'),
			(u'気','CJK Unified Ideographs'),
			(u'の','Hiragana'),
			(u'ト','Katakana'),
			(u'ಠ','Kannada'),
		]
		for i,e in testcases:
			self.assertEqual(block(i),e)
	
	def test_block_error(self):
		"""Test block() with invalid argument"""
		self.assertRaises(TypeError, block, (5,))
		self.assertRaises(TypeError, block, ('a',))
		self.assertRaises(TypeError, block, (u'abc',))
	
	def test_script_error(self):
		"""Test script() with invalid argument"""
		self.assertRaises(TypeError, script, (5,))
		self.assertRaises(TypeError, script, ('a',))
		self.assertRaises(TypeError, script, (u'abc',))
	
	def test_latin_letters(self):
		"""Test script: Latin"""
		testcases = u'aAåÅăĂąĄẬậɑⱭɐⱯæÆéÉèÈȄȅḿḾøØœŒÿŸ'
		for c in testcases:
			self.assertEqual(script(c, avoid_common=True), 'Latin')
			self.assertEqual(script(c, avoid_common=False), 'Latin')
	
	def test_latin_letters_cached(self):
		"""Test script: Latin (cached)"""
		testcases = u'aabbaaaa'
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