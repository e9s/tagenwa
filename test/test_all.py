# -*- coding: UTF-8 -*-
import unittest

import test_util
import test_uniscript
import test_token
import test_pre
import test_retokenizer_dictionary

all_tests = unittest.TestSuite([
	test_util.suite(),
	test_uniscript.suite(),
	test_token.suite(),
	test_pre.suite(),
	test_retokenizer_dictionary.suite(),
])

if __name__ == '__main__':
	unittest.TextTestRunner(verbosity=2).run(all_tests)