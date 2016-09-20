import unittest

from config import APP_ROOT
from joseph.config import Config
from joseph.exceptions import JosephConfigException


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

    def test_default_kwargs(self):
        self.config = Config(APP_ROOT, foo='bar')
        self.assertTrue('foo' in self.config.keys())
        self.assertEqual(self.config['foo'], 'bar')

    def test_from_file(self):
        self.config.from_file('config.py')
        self.assertTrue('DEBUG' in self.config.keys())
        self.assertEqual(True, self.config['DEBUG'])

    def test_from_file_not_existing(self):
        with self.assertRaises(JosephConfigException):
            self.config.from_file('foo.bar')

    def test_proxy(self):
        import types
        proxy = self.config.proxy

        self.assertTrue('foo' in proxy.keys())
        self.assertIsInstance(proxy, types.MappingProxyType)

        self.assertEqual('bar', proxy['foo'])
        with self.assertRaises(TypeError):
            proxy['foo'] = 'baz'

    def test_get_items(self):
        self.assertEqual('bar', self.config['foo'])
        self.assertEqual('bar', self.config.foo)

    def test_set_items(self):
        self.config['foo'] = 'baz'
        self.assertEqual('baz', self.config['foo'])

        self.config.foo = 'joseph'
        self.assertEqual('joseph', self.config.foo)
