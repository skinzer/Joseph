import unittest

from joseph.helpers import Stack


class TestStack(unittest.TestCase):
    def setUp(self):
        self.stack = Stack('foo', 'bar')

    def tearDown(self):
        del self.stack

    def test_test(self):
        self.assertTrue(True)

    def test_init(self):
        self.assertIsInstance(self.stack, Stack)
        self.assertIn('foo', self.stack)
        self.assertIn('bar', self.stack)
        self.assertNotIn('baz', self.stack)

    def test_append(self):
        self.stack.append('baz')
        self.assertIn('baz', self.stack)

    def test_del_(self):
        self.stack.del_('bar')
        self.assertNotIn('bar', self.stack)

        with self.assertRaises(ValueError):
            self.stack.del_('baz')

    def test_pop_(self):
        foo = self.stack.pop_('foo')
        self.assertEqual(foo, 'foo')
        self.assertNotIn('foo', self.stack)

        with self.assertRaises(ValueError):
            baz = self.stack.pop_('baz')
