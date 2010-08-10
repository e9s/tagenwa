# -*- coding: UTF-8 -*-
import unittest

import test_util
import test_uniscript
import test_token
import test_trie
import test_pre
import test_retokenizer_dictionary

all_tests = unittest.TestSuite([
	test_util.suite(),
	test_uniscript.suite(),
	test_token.suite(),
	test_trie.suite(),
	test_pre.suite(),
	test_retokenizer_dictionary.suite(),
])

def test_all():
	unittest.TextTestRunner(verbosity=2).run(all_tests)

if __name__ == '__main__':
	test_all()