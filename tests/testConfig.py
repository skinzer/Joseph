import os
import shutil
import types

import asynctest

try:
    from config import APP_ROOT
except ImportError:
    import imp

    APP_ROOT = imp.load_source('config', 'config.default.py').APP_ROOT

from joseph.config import Config
from joseph.exceptions import ConfigException


class TestConfig(asynctest.TestCase):
    environment_variables = ["JOSEPH_TEST", "FOOBAR"]
    use_default_loop = True
    forbid_get_event_loop = False

    _delete_config_file = False

    def setUp(self):
        self.config = Config(APP_ROOT, {'FOO': 'bar'})
        for var in self.environment_variables:
            os.environ[var] = "foobar"

    def tearDown(self):
        del self.config
        for var in self.environment_variables:
            try:
                del os.environ[var]
            except KeyError:
                continue

        if self._delete_config_file and os.path.isfile(self.config_path):
            os.remove(self.config_path)

    @property
    def config_path(self):
        return os.path.join(APP_ROOT, "config.py")

    @property
    def default_config_path(self):
        return os.path.join(APP_ROOT, "config.default.py")

    def setUpConfigFile(self):
        if not os.path.isfile(self.config_path):
            shutil.copy(self.default_config_path, self.config_path)
            self._delete_config_file = True

    @asynctest.fail_on(unused_loop=False)
    def test_test(self):
        self.assertTrue(True)

    @asynctest.fail_on(unused_loop=False)
    def test_default_dict(self):
        self.assertIn("FOO", self.config.keys())
        self.assertEqual("bar", self.config['FOO'])

        with self.assertRaises(KeyError):
            var = self.config['BAR']

    @asynctest.fail_on(unused_loop=False)
    def test_named_arguments(self):
        self.config = Config(TEST_1="foo", TEST_2="bar")
        self.assertIn("TEST_1", self.config.keys())
        self.assertEqual("foo", self.config['TEST_1'])
        self.assertEqual("bar", self.config['TEST_2'])

        with self.assertRaises(KeyError):
            var = self.config['TEST_3']

    @asynctest.fail_on(unused_loop=False)
    def test_setitem(self):
        self.config['BAZ'] = 123
        self.assertEqual(self.config['BAZ'], 123)

        # Lower case keys should not be allowed
        with self.assertRaises(ConfigException):
            self.config['baz'] = 456

    @asynctest.fail_on(unused_loop=False)
    def test_setattr(self):
        self.config.FOO = 1
        self.assertIn("FOO", self.config.keys())

        self.config.bar = 2
        self.assertEqual(self.config.bar, 2)
        self.assertIn("bar", dir(self.config))
        self.assertNotIn("bar", self.config.keys())

        with self.assertRaises(KeyError):
            var = self.config['bar']

    @asynctest.fail_on(unused_loop=False)
    def test_getattr(self):
        self.config.foo = 9
        self.assertEqual(self.config.foo, 9)

        self.config['BAR'] = 789
        self.assertEqual(self.config.BAR, 789)

        with self.assertRaises(ConfigException):
            self.config['baz'] = 123

        with self.assertRaises(AttributeError):
            var = self.config.baz

    @asynctest.fail_on(unused_loop=False)
    def test_keys(self):
        self.config = Config(TEST_1=123, TEST_2=456, test_3=789)

        self.assertIsInstance(self.config.keys(), list)
        self.assertIn("TEST_1", self.config.keys())
        self.assertIn("TEST_2", self.config.keys())
        self.assertNotIn("TEST_3", self.config.keys())

    @asynctest.fail_on(unused_loop=False)
    def test_values(self):
        self.config = Config(TEST_1=123, TEST_2=456, test_3=789)

        self.assertIsInstance(self.config.values(), list)
        self.assertIn(123, self.config.values())
        self.assertIn(456, self.config.values())
        self.assertNotIn(789, self.config.values())

    @asynctest.fail_on(unused_loop=False)
    def test_items(self):
        self.config = Config(TEST_1=123, TEST_2=456, test_3=789)

        self.assertIsInstance(self.config.items(), dict)
        self.assertIn("TEST_1", self.config.items())
        self.assertIn("TEST_2", self.config.items())
        self.assertNotIn("test_3", self.config.items())

        self.assertIn(123, self.config.items().values())
        self.assertIn(456, self.config.items().values())
        self.assertNotIn(789, self.config.items().values())

    @asynctest.fail_on(unused_loop=False)
    def test_proxy(self):
        self.config = Config(TEST_1=123, TEST_2=456, test_3=789)
        self.assertIsInstance(self.config.proxy, types.MappingProxyType)

        proxy = self.config.proxy
        self.assertIn("TEST_1", proxy.keys())
        self.assertIn(456, proxy.values())

        with self.assertRaises(TypeError):
            proxy['TEST_1'] = 123

    def test_from_file(self):
        self.setUpConfigFile()

        # Not a particularly good idea
        self.config['WORKER_COUNT'] = 99

        proxy = self.loop.run_until_complete(self.config.from_file())
        self.assertIsInstance(proxy, types.MappingProxyType)

        self.assertIn("WORKER_COUNT", self.config.keys())
        self.assertIn("DEBUG", self.config.keys())

        self.assertIsInstance(self.config['WORKER_COUNT'], int)
        self.assertNotEqual(self.config['WORKER_COUNT'], 99)
        self.assertIsInstance(self.config['DEBUG'], bool)

    def test_from_not_existing_file(self):
        with self.assertRaises(ConfigException):
            self.loop.run_until_complete(self.config.from_file(filename='foo.bar'))

        self.assertNotIn("WORKER_COUNT", self.config.keys())
        self.assertNotIn("DEBUG", self.config.keys())

    def test_from_not_existing_file_silent(self):
        self.config['WORKER_COUNT'] = 99
        # Should silently fail so the keys should not be available
        self.loop.run_until_complete(self.config.from_file(filename='foo.bar', silent=True))

        self.assertNotIn("DEBUG", self.config.keys())
        self.assertEqual(self.config['WORKER_COUNT'], 99)

    def test_from_env_vars(self):
        self.loop.run_until_complete(self.config.from_env_vars())

        self.assertIn("TEST", self.config.keys())
        self.assertEqual("foobar", self.config['TEST'])

        self.assertNotIn("FOOBAR", self.config.keys())

    @asynctest.fail_on(unused_loop=False)
    def test_repr(self):
        self.assertIsInstance(self.config.__repr__(), str)
