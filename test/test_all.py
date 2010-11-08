# -*- coding: UTF-8 -*-
import unittest

import test_tools
import test_uniscript
import test_token
import test_pre
import test_ngram
import test_trie
import test_retokenizer_dictionary
import test_retokenizer_number

all_tests = unittest.TestSuite([
	test_tools.suite(),
	test_uniscript.suite(),
	test_token.suite(),
	test_pre.suite(),
	test_ngram.suite(),
	test_trie.suite(),
	test_retokenizer_dictionary.suite(),
	test_retokenizer_number.suite(),
])

def test_all():
	unittest.TextTestRunner(verbosity=2).run(all_tests)

if __name__ == '__main__':
	test_all()