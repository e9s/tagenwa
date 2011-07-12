# -*- coding: UTF-8 -*-
import unittest, doctest
import unicodedata

from tagenwa.text.normalize import remove_combining_marks, remove_ligatures, collapse_spaces, normalize_eol

class TestNormalize(unittest.TestCase):	
	
	def test_util_doctest(self):
		import tagenwa.text.normalize
		failure_count, test_count = doctest.testmod(tagenwa.text.normalize)
		self.assertEqual(failure_count, 0, 'Testing doctest from tagenwa.text.normalize: %i failed out of %i' % (failure_count, test_count))
	
	
	def test_combining_marks(self):
		testcases = [
			(u'', u''),
			(u'café',u'cafe'),
			(u'ça',u'ca'),
		]
		for i,e in testcases:
			self.assertEqual(e, remove_combining_marks(i))
	
	
	def test_ligatures(self):
		testcases = [
			#(u'straß',u'strass'),
			(u'ex æquo',u'ex aequo'),
			(u'œuf',u'oeuf'),
			(u'Œuf',u'OEuf'),
			(u'vrĳ',u'vrij'),
		]
		for i,e in testcases:
			self.assertEqual(e, remove_ligatures(unicodedata.normalize('NFC',i)))
	
	
	def test_normalize_eol(self):
		testcases = [
			(u'\n', u'\n'),
			(u'\r',u'\n'),
			(u'\r\n',u'\n'),
		]
		for i,e in testcases:
			self.assertEqual(e, normalize_eol(i))
	
	

def suite():
	suite = unittest.TestSuite([
		unittest.TestLoader().loadTestsFromTestCase(TestNormalize),
	])
	return suite

if __name__ == '__main__':
	unittest.main()	
