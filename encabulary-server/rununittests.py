import unittest

import xmlrunner

runner = xmlrunner.XMLTestRunner('tests_xml', verbosity=2)

runner.run(unittest.TestLoader().discover('server/tests/functional_tests'))
