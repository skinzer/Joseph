import os
import shutil
import unittest

from config import APP_ROOT
from joseph.entities import EntityManager
from joseph.entities.types import Entity
from joseph.helpers import Stack


class TestEntity(Entity):
    """
    Subclasses :class:`Entity` for testing alternative entity types
    """
    pass

class TestEntityManager(unittest.TestCase):
    def setUp(self):
        self.em = EntityManager(APP_ROOT)
        self.entity = Entity(name='test_entity', data={'foo': 123, 'bar': 456})

    def tearDown(self):
        # Delete all test files that may have been created
        for file in os.listdir(self.em.data_dir):
            if file.startswith('test'):
                try:
                    shutil.rmtree(os.path.join(self.em.data_dir, file))

                except NotADirectoryError:
                    os.remove(os.path.join(self.em.data_dir, file))

        del self.em
        del self.entity

    def test_test(self):
        self.assertTrue(True)

    def test_init(self):
        self.assertIsInstance(self.em, EntityManager)
        self.assertIsInstance(self.em.collection, dict)
        self.assertIsInstance(self.em.collection[''], Stack)

        data_dir = os.path.join(APP_ROOT, 'data')
        self.assertEqual(self.em.data_dir, data_dir)

    def test_register_in_collection(self):
        self.em._register_entity_in_collection(self.entity)
        self.assertTrue(self.entity in self.em.collection[''])

        # Test an entity that's a subclass of Entity
        test_entity = TestEntity(name='test_entity',
                                 data={'foo': 123, 'bar': 456})
        self.em._register_entity_in_collection(test_entity)
        self.assertTrue(test_entity in self.em.collection['test_entity'])

    def test_write_to_file(self):
        self.em.write_to_file(self.entity)
        path = os.path.join(self.em.data_dir,
                            '{0}.{1}'.format(self.entity.filename,
                                             self.em.file_ext))
        self.assertTrue(os.path.exists(path))

    def test_construct_from_file(self):
        # Make sure test_file.yml exists
        self.test_write_to_file()

        entity = self.em._construct_from_file('test_entity', Entity, True)
        self.assertIsInstance(entity, Entity)
        self.assertEqual(entity.bar, 456)

        with self.assertRaises(FileNotFoundError):
            entity = self.em._construct_from_file('not_existing', Entity, True)

    def test_construct_new_entity(self):
        entity = self.em._construct_new_entity('baz', Entity, {'foo': 123, 'bar': 456})
        self.assertIsInstance(entity, Entity)
        self.assertEqual(entity.foo, 123)

    def test_construct_existing(self):
        # Should load entity from file
        test_entity = TestEntity(name='test_entity',
                         data={'foo': 123, 'bar': 456})
        self.em.write_to_file(test_entity)

        entity = self.em.construct('test_entity')
        self.assertIsInstance(entity, Entity)
        self.assertEqual(test_entity.foo, 123)

    def test_construct_not_existing(self):
        entity = self.em.construct('test_new_entity')
        entity = self.assertIsInstance(entity, Entity)

    def test_delete_entity_from_collection(self):
        entity = self.em.construct('test_entity')
        self.assertIn(entity, self.em.collection[''])

        self.em._delete_entity_from_collection(entity)

        with self.assertRaises(KeyError):
            self.assertFalse(entity in self.em.collection[''])

    def test_delete_entity_file(self):
        self.em.write_to_file(self.entity)
        path = os.path.join(self.em.data_dir,
                            '{0}.{1}'.format(self.entity.filename,
                                             self.em.file_ext))
        self.assertTrue(os.path.exists(path))

        self.em._delete_entity_file(self.entity)
        self.assertFalse(os.path.exists(path))

    def test_delete_subclass_entity_file(self):
        test_entity = self.em._construct_new_entity('test_entity',
                                                    TestEntity,
                                                    data={'foo': 123, 'bar': 456})
        self.em.write_to_file(test_entity)
        path = os.path.join(self.em.data_dir,
                            '{0}.{1}'.format(test_entity.filename,
                                             self.em.file_ext))
        self.assertTrue(os.path.exists(path))

        self.em._delete_entity_file(test_entity)
        self.assertFalse(os.path.exists(path))

    def test_delete_subclass_entity_from_collection(self):
        test_entity = self.em._construct_new_entity('test_entity',
                                                    TestEntity,
                                                    data={'foo': 123, 'bar': 456})

        self.em._register_entity_in_collection(test_entity)
        self.assertIn(test_entity, self.em.collection['test_entity'])
        self.em._delete_entity_from_collection(test_entity)

        with self.assertRaises(KeyError):
            self.assertFalse(test_entity in self.em.collection['test_entity'])

    def test_delete_entity(self):
        self.em.write_to_file(self.entity)
        path = os.path.join(self.em.data_dir,
                            '{0}.{1}'.format(self.entity.filename,
                                             self.em.file_ext))
        self.assertTrue(os.path.exists(path))

        self.em._register_entity_in_collection(self.entity)
        self.em.delete(self.entity)

        with self.assertRaises(KeyError):
            self.assertFalse(self.entity in self.em.collection[''])

        self.assertFalse(os.path.exists(path))

    def test_delete_subclass_entity(self):
        test_entity = self.em.construct('test_entity', entity=TestEntity,
                                        data={'foo': 123, 'bar': 456})

        path = os.path.join(self.em.data_dir,
                            '{0}.{1}'.format(test_entity.filename,
                                             self.em.file_ext))
        self.assertTrue(os.path.exists(path))
        self.assertTrue(test_entity in self.em.collection[test_entity.entity_type])

        self.em.delete(test_entity)

        with self.assertRaises(KeyError):
            self.assertFalse(test_entity in self.em.collection[test_entity.entity_type])

        self.assertFalse(os.path.exists(path))

    def test_delete_entity_not_silent(self):
        # File is never written, so we can test if the proper error is raised
        test_entity = TestEntity(name='test_entity', data={'foo': 123, 'bar': 456})

        with self.assertRaises(FileNotFoundError):
            self.em._delete_entity_file(test_entity, silent=False)

    def test_delete_entity_empty_dir(self):
        test_entity = self.em.construct('test_entity', entity=TestEntity,
                                        data={'foo': 123, 'bar': 456})

        path = os.path.join(self.em.data_dir,
                            '{0}.{1}'.format(test_entity.filename,
                                             self.em.file_ext))
        self.assertTrue(os.path.exists(path))

        self.em.delete(test_entity, delete_empty_dir=False)
