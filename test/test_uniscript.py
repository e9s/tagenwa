# -*- coding: UTF-8 -*-
import unittest, doctest

from tagenwa.uniscript import script, block


class TestScript(unittest.TestCase):
	
	def test_uniscript_doctest(self):
		"""Test uniscript doctests"""
		import tagenwa.uniscript
		failure_count, test_count = doctest.testmod(tagenwa.uniscript)
		self.assertEqual(failure_count, 0, 'Testing doctest from tagenwa.uniscript: %i failed out of %i' % (failure_count, test_count))
	
	
	def test_block(self):
		"""Test uniscript.block()"""
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
			(u'ａ','Halfwidth and Fullwidth Forms'),
			(u'の','Hiragana'),
			(u'ト','Katakana'),
			(u'ಠ','Kannada'),
		]
		for i,e in testcases:
			self.assertEqual(block(i),e)
	
	def test_block_error(self):
		"""Test uniscript.block() with invalid argument"""
		self.assertRaises(TypeError, block, (5,))
		self.assertRaises(TypeError, block, ('a',))
		self.assertRaises(TypeError, block, (u'abc',))
	
	def test_script_error(self):
		"""Test uniscript.script() with invalid argument"""
		self.assertRaises(TypeError, script, (5,))
		self.assertRaises(TypeError, script, ('a',))
		self.assertRaises(TypeError, script, (u'abc',))
	
	def test_latin_letters(self):
		"""Test uniscript.script() with Latin"""
		testcases = u'aAåÅăĂąĄẬậɑⱭɐⱯæÆéÉèÈȄȅḿḾøØœŒÿŸ'
		for c in testcases:
			self.assertEqual(script(c, avoid_common=True), 'Latin')
			self.assertEqual(script(c, avoid_common=False), 'Latin')
	
	def test_cjk(self):
		"""Test uniscript.script() with Han"""
		testcases = u'気氣'
		for c in testcases:
			self.assertEqual(script(c, avoid_common=True), 'Han')
			self.assertEqual(script(c, avoid_common=False), 'Han')
	
	def test_hiragana(self):
		"""Test uniscript.script() with Hiragana"""
		testcases = u'あいうえおはばぱをん'
		for c in testcases:
			self.assertEqual(script(c, avoid_common=True), 'Hiragana')
			self.assertEqual(script(c, avoid_common=False), 'Hiragana')
	
	def test_katakana(self):
		"""Test uniscript.script() with Katakana"""
		testcases1 = u'アイウエオハパバヲン'
		for c in testcases1:
			self.assertEqual(script(c, avoid_common=False), 'Katakana')
		testcases2 = u'ー'
		for c in testcases1+testcases2:
			self.assertEqual(script(c, avoid_common=True), 'Katakana')
	
	def test_katakana_halfwidth(self):
		"""Test uniscript.script() with Katakana halfwidth"""
		testcases = u'ｶﾀｶﾅ'
		for c in testcases:
			self.assertEqual(script(c, avoid_common=False), 'Katakana')
			self.assertEqual(script(c, avoid_common=True), 'Katakana')
	
	def test_latin_fullwidth(self):
		"""Test uniscript.script() with Latin fullwidth"""
		testcases = u'ａＡ'
		for c in testcases:
			self.assertEqual(script(c, avoid_common=False), 'Latin')
			self.assertEqual(script(c, avoid_common=True), 'Latin')


def suite():
	suite = unittest.TestLoader().loadTestsFromTestCase(TestScript)
	return suite

if __name__ == '__main__':
	unittest.main()