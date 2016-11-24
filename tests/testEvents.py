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


class TestEvent(unittest.TestCase):
    def setUp(self):
        self.namespace = Namespace("tests")
        self.event = self.namespace.make_event("foo")

    def tearDown(self):
        del self.namespace
        del self.event

    def test_test(self):
        self.assertTrue(True)

    def test_init(self):
        self.assertIsInstance(self.namespace, Namespace)
        self.assertIsInstance(self.event, Event)

    def test_hash(self):
        event = Event(self.namespace, "foo")
        self.assertEqual(hash(self.event), hash(event))

        event = Event(self.namespace, "foo", strict=True, bar=123)
        self.assertNotEqual(hash(self.event), hash(event))

    def test_string(self):
        self.assertEqual(str(self.event), "tests:foo")
        self.assertNotEqual(str(self.event), "foo:bar")

        event = self.namespace.make_event()
        self.assertEqual(str(event), "tests")
        self.assertNotEqual(str(event), "tests:foo")

    def test_eq(self):
        event = self.namespace.make_event("foo")
        self.assertEqual(self.event, event)

        event = self.namespace.make_event("bar")
        self.assertNotEqual(self.event, event)

        event = self.namespace.make_event("foo", bar=123, strict=False)
        event2 = self.namespace.make_event("foo", bar=123, strict=False)
        self.assertEqual(event, event2)

        event = self.namespace.make_event("foo", bar=123, strict=False)
        event2 = self.namespace.make_event("foo", bar=456, strict=False)
        self.assertEqual(event, event2)

        event = self.namespace.make_event("foo", bar=123, strict=True)
        event2 = self.namespace.make_event("foo", bar=456, strict=False)
        self.assertNotEqual(event, event2)
