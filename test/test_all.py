# -*- coding: UTF-8 -*-
import unittest

import test_uniscript
import test_token
import test_pre

all_tests = unittest.TestSuite([
	
	test_uniscript.suite(),
	test_token.suite(),
	test_pre.suite(),
])

if __name__ == '__main__':
	unittest.TextTestRunner(verbosity=2).run(all_tests)