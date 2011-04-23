# -*- coding: UTF-8 -*-
import unittest, doctest

from tagenwa.text.script import script, block


class TestScript(unittest.TestCase):
	
	
	def test_unicodescript_doctest(self):
		"""Test uniscript doctests"""
		import tagenwa.unicodescript
		failure_count, test_count = doctest.testmod(tagenwa.unicodescript)
		self.assertEqual(failure_count, 0, 'Testing doctest from tagenwa.unicodescript: %i failed out of %i' % (failure_count, test_count))
	
	
	def test_block(self):
		"""Test unicodescript.block()"""
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
		"""Test unicodescript.block() with invalid argument"""
		self.assertRaises(TypeError, block, (5,))
		self.assertRaises(TypeError, block, ('a',))
		self.assertRaises(TypeError, block, (u'abc',))
	
	
	def test_script_error(self):
		"""Test unicodescript.script() with invalid argument"""
		self.assertRaises(TypeError, script, (5,))
		self.assertRaises(TypeError, script, ('a',))
		self.assertRaises(TypeError, script, (u'abc',))
	
	
	def test_latin_letters(self):
		"""Test unicodescript.script() with Latin"""
		testcases = u'aAåÅăĂąĄẬậɑⱭɐⱯæÆéÉèÈȄȅḿḾøØœŒÿŸ'
		for c in testcases:
			self.assertEqual(script(c), 'Latin')
	
	
	def test_cjk(self):
		"""Test unicodescript.script() with Han"""
		testcases = u'気氣'
		for c in testcases:
			self.assertEqual(script(c), 'Han')
	
	
	def test_hiragana(self):
		"""Test unicodescript.script() with Hiragana"""
		testcases = u'あいうえおはばぱをん'
		for c in testcases:
			self.assertEqual(script(c), 'Hiragana')
	
	
	def test_katakana(self):
		"""Test unicodescript.script() with Katakana"""
		testcases1 = u'アイウエオハパバヲン'
		for c in testcases1:
			self.assertEqual(script(c), 'Katakana')
		testcases2 = u'ー'
		for c in testcases2:
			self.assertEqual(script(c), 'Katakana')
	
	
	def test_katakana_halfwidth(self):
		"""Test unicodescript.script() with Katakana halfwidth"""
		testcases = u'ｶﾀｶﾅ'
		for c in testcases:
			self.assertEqual(script(c), 'Katakana')
	
	
	def test_latin_fullwidth(self):
		"""Test unicodescript.script() with Latin fullwidth"""
		testcases = u'ａＡ'
		for c in testcases:
			self.assertEqual(script(c), 'Latin')


def suite():
	suite = unittest.TestLoader().loadTestsFromTestCase(TestScript)
	return suite

if __name__ == '__main__':
	unittest.main()