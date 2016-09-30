import os
import types
import unittest

from config import APP_ROOT

from joseph.entities.types import PluginType
from joseph.plugins import PluginManager
from joseph.helpers.stack import Stack


class TestPluginManager(unittest.TestCase):
    def setUp(self):
        self.pm = PluginManager(APP_ROOT)
        self.plugin_dir = os.path.join(APP_ROOT, 'plugins')

        self.test_plugin = """def run():\n\treturn 'test'"""

        with open(os.path.join(self.plugin_dir, 'test_plugin.py'), 'w') as file:
            file.write(self.test_plugin)

    def tearDown(self):
        for file in os.listdir(self.plugin_dir):
            if file.startswith('test'):
                os.remove(os.path.join(self.plugin_dir, file))

        del self.pm

    def test_test(self):
        self.assertTrue(True)

    def test_init(self):
        self.assertIsInstance(self.pm, PluginManager)
        self.assertIsInstance(self.pm.not_run, Stack)

        plugin_dir = os.path.join(APP_ROOT, 'plugins')
        self.assertEqual(self.pm.plugin_dir, plugin_dir)

    def test_discover(self):
        """
        Test plain discovery without `auto_compile` or
        `auto_run` functionality
        """
        discovered = self.pm.discover(auto_compile=False)
        self.assertIsInstance(discovered, types.GeneratorType)
