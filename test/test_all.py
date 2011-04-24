# -*- coding: UTF-8 -*-
import unittest

import test_langid_ngram
import test_text_normalize
import test_text_script
import test_text_token
import test_tokenize_dictionary
import test_tokenize_treebank
import test_utils_iterators
import test_utils_trie

all_tests = unittest.TestSuite([
	test_langid_ngram.suite(),
	test_text_normalize.suite(),
	test_text_script.suite(),
	test_text_token.suite(),
	test_tokenize_dictionary.suite(),
	test_tokenize_treebank.suite(),
	test_utils_iterators.suite(),
	test_utils_trie.suite(),
])

def test_all():
	unittest.TextTestRunner(verbosity=2).run(all_tests)

if __name__ == '__main__':
	test_all()