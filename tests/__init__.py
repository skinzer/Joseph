"""
Run from project root

Usage:
    from tests import tests, runner
    runner.run(tests)
"""

import unittest

loader = unittest.TestLoader()
tests = loader.discover('.')

runner = unittest.runner.TextTestRunner()
