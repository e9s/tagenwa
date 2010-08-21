# -*- coding: UTF-8 -*-
import unittest, doctest


class TestNgram(unittest.TestCase):
	
	def test_ngram_doctest(self):
		import tagenwa.langid.ngram
		failure_count, test_count = doctest.testmod(tagenwa.langid.ngram)
		self.assertEqual(failure_count, 0, 'Testing doctest from tagenwa.langid.ngram: %i failed out of %i' % (failure_count, test_count))


def suite():
	suite = unittest.TestLoader().loadTestsFromTestCase(TestNgram)
	return suite

if __name__ == '__main__':
	unittest.main()
