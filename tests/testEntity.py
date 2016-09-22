import unittest

from joseph.entities.types import Entity


class FooEntity(Entity):
    pass


class TestEntity(unittest.TestCase):
    def setUp(self):
        self.entity = Entity(name='test_entity', data={'foo': 123, 'bar': 456})

    def tearDown(self):
        del self.entity

    def test_test(self):
        self.assertTrue(True)

    def test_init(self):
        self.assertIsInstance(self.entity, Entity)
        self.assertEqual(self.entity.foo, 123)

        with self.assertRaises(AttributeError):
            self.entity.baz

    def test_entity_type(self):
        self.assertEqual(self.entity.entity_type, 'entity')

        foo = FooEntity(name='test_entity', data={'foo': 123, 'bar': 456})
        self.assertEqual(foo.entity_type, 'foo_entity')

    def test_dict_like(self):
        self.assertEqual(self.entity['foo'], 123)
        with self.assertRaises(KeyError):
            self.entity['baz']

        self.entity['baz'] = 789
        self.assertEqual(self.entity['baz'], 789)

    def test_filename(self):
        self.assertEqual(self.entity.filename, 'test_entity')

        foo = FooEntity(name='test_entity', data={'foo': 123, 'bar': 456})
        self.assertEqual(foo.filename, 'foo_entity\\test_entity')
