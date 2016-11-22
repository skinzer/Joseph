import unittest

from joseph.events import Event, Namespace


class TestNamespace(unittest.TestCase):
    def setUp(self):
        self.namespace = Namespace("tests")

    def tearDown(self):
        del self.namespace

    def test_init(self):
        self.assertIsInstance(self.namespace, Namespace)

        self.namespace = Namespace()
        self.assertIsInstance(self.namespace, Namespace)
        self.assertEqual(str(self.namespace), "testEvents")

    def test_make_event(self):
        event_1 = self.namespace.make_event("test")
        self.assertIsInstance(event_1, Event)

        event_2 = self.namespace.make_event("")
        self.assertIsInstance(event_2, Event)

        event_3 = self.namespace.make_event("test", foo="bar")
        self.assertIn("foo", dir(event_3))

        with self.assertRaises(TypeError):
            event_4 = self.namespace.make_event()

    def test_test(self):
        self.assertTrue(True)

    def test_hash(self):
        self.assertEqual(hash(self.namespace), hash("tests"))
        self.assertNotEqual(hash(self.namespace), hash("foobar"))

    def test_string(self):
        self.assertEqual(str(self.namespace), "tests")
        self.assertNotEqual(str(self.namespace), "foobar")

    def test_equal(self):
        test_namespace = Namespace("tests")
        self.assertEqual(self.namespace, test_namespace)

        test_namespace = Namespace("foo")
        self.assertNotEqual(self.namespace, test_namespace)
