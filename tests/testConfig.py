import unittest

from config import APP_ROOT
from joseph.config import Config


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.config = Config(APP_ROOT, {'foo': 'bar'})

    def tearDown(self):
        del self.config

    def test_test(self):
        self.assertTrue(True)

    def test_default_dict(self):
        self.config = Config(APP_ROOT, {'foo': 'bar'})
        self.assertTrue('foo' in self.config.keys())
        self.assertEqual(self.config['foo'], 'bar')
