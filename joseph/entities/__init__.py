import os
import shutil

import yaml

from .types import EntityType
from ..helpers import Stack, camel_to_snake


class EntityManager(object):
    """
    Joseph's entity manager

    Manages Joseph's YAML based entities. The manager is able to create
    entities from a file using the :meth:`_construct_from_file` or by
    creating a new entity based on existing parameters using
    :meth:`_construct_new_entity`. Both methods can be called easily
    using :meth:`construct`.

    Entities are stored in a dict at :property:`collection` which uses
    the entity's class name as a key, this key is then also used as a folder
    name. Compared to a 'regular' database, these keys would be the entity's
    table.

    As writing to the file system can be a relatively costly activity, a
    session will be implemented in the future. This will make it possible
    to take the performance hit later on.

    TODO:
        - YAML queries
        - Implement a session
    """

    def __init__(self, app_root, data_dir='data', file_ext='yml'):
        self.app_root = app_root
        self.data_dir = os.path.join(self.app_root, data_dir)
        self.file_ext = file_ext
        self.collection = {
            '': Stack()
        }

    def _construct_from_file(self, name, entity, safe_load):
        """
		Constructs an entity objects from a file using the yaml
		module.

        TODO:
            - Entity type loading

		:param name: Name of object, this is also the name of the yaml file
		:param entity: Class of the entity to return
		:param safe_load: `True` / `False` sets whether ``yaml.safe_load`` is
		 				  is used.
		:return: Entity with data read from file
		"""
        filename = '{0}.{1}'.format(name, self.file_ext)

        if entity.__name__ == 'Entity':
            filename = os.path.join(self.data_dir, filename)

        else:
            filename = os.path.join(self.data_dir,
                                    camel_to_snake(entity.__name__),
                                    filename)

        with open(filename, 'r') as file:
            if safe_load:
                payload = yaml.safe_load(file)

            else:
                payload = yaml.load(file)

        if isinstance(payload, dict) and len(payload) > 0:
            entity = entity(name=name, data=payload)

        else:
            raise FileNotFoundError('File {} does not exist or is empty'.format(filename))

        return entity

    def _construct_new_entity(self, name, entity, data):
        """
		Builds new entity from the provided parameters after
		creation the entity is registered on the stack.

		:param name: Name of the entity as string
		:param entity: Class of the object
		:param data: Initial values of entity
		:return: Created entity
		"""
        entity = entity(name=name, data=data)

        return entity

    def _register_entity_in_collection(self, entity):
        """
        Registers the entity in the collection using the :param:`entity`'s'
        :property:`entity_type` as the key.

        :param entity: Entity to register
        """
        if not isinstance(entity, Entity):
            raise ValueError('Expected parameter \'entity\' as a parameter')

        if entity.entity_type == 'entity':
            entity_type = ''

        else:
            entity_type = entity.entity_type

        try:
            self.collection[entity_type].append(entity)

        except KeyError:
            self.collection[entity_type] = Stack(entity)

    def construct(self, name, entity=Entity, safe_load=True, data=None):
        """
		Provides access to :meth: `_construct_from_file` and
		:meth: `_construct_new_entity`.

		Tries to load values from a yaml file using :param:`name`,
		if it fails, it assumes a new entity should be created.

        TODO:
            - Find file by entity type

		:param name: Name of the entity
		:param entity: Class of the entity
		:param safe_load: Tells :meth:`_construct_from_file` if
						  ``yaml.safe_load`` should be used.
		:param data: Dict to be used for the new entity
		:return: Created entity
		"""
        try:
            entity = self._construct_from_file(name, entity, safe_load)

        except FileNotFoundError:
            if not data:
                data = {}

            entity = self._construct_new_entity(name, entity, data=data)
            self.write_to_file(entity)

        self._register_entity_in_collection(entity)

        return entity

    def _delete_entity_from_collection(self, entity, silent=True):
        """
        Delete entity from the collection, if this :meth: is called
        silently and an error occurs `False` is returned

        :param entity: Entity to delete
        :param silent: Ignores errors if `True`
        :return: `True` / `False`
        """

        if entity.entity_type == 'entity':
            entity_type = ''

        else:
            entity_type = entity.entity_type

        try:
            self.collection[entity_type].del_(entity)

            if len(self.collection[entity_type]) == 0:
                del self.collection[entity_type]

        except IndexError as e:
            if not silent:
                raise IndexError(e)

            else:
                return False

        return True

    def _delete_entity_file(self, entity, silent=False, delete_empty_dir=True):
        """
        Deletes the entity's yaml file from the filesystem

        :param entity: Entity to delete
        :param silent: Ignore errors if True
        :param delete_empty_dir: Delete directory if it's empty after removing
                                 entity file.
        """
        filename = os.path.join(self.data_dir,
                                '{0}.{1}'.format(entity.filename, self.file_ext))

        dirname = os.path.dirname(filename)

        try:
            os.remove(filename)

        except FileNotFoundError as e:
            if not silent:
                raise FileNotFoundError(e)

        if delete_empty_dir:
            if os.listdir(dirname) == []:
                try:
                    shutil.rmtree(dirname, ignore_errors=True)

                except FileNotFoundError as e:
                    if not silent:
                        raise FileNotFoundError(e)

    def delete(self, entity, delete_empty_dir=True, silent=True):
        """
		Provides a front to :meth:`_delete_entity_from_collection` and
        :meth:`_delete_entity_file`.

		:param entity: Entity to delete
		"""

        if self._delete_entity_from_collection(entity, silent=silent):
            self._delete_entity_file(entity, delete_empty_dir=delete_empty_dir, silent=silent)

    def delete_all(self, entities):
        """
        Like :meth:`delete` but takes an iterable containing entities and
        iters over it. For each item the :meth:`delete` is called.

        :param entities: Iterable with entities to delete
        """
        for entity in entities:
            self.delete(entity)

    def write_to_file(self, entity):
        """
		Gets the :param:`entity` relative path and combines with the
        :property:`data_dir` and :property:`file_ext` to get full path.

        Once the path is complete the :param:`entity` is written to the file

		:param entity: Entity to write to file
		"""

        filename = os.path.join(self.data_dir, '{0}.{1}'.format(entity.filename,
                                                                self.file_ext))

        dirname = os.path.dirname(filename)

        if not os.path.exists(dirname):
            os.makedirs(dirname)

        with open(filename, 'w') as file:
            yaml.dump(entity.__dict__, file, default_flow_style=False)
