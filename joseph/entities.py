import os
import yaml

from .exceptions import JosephFileNotFound


class Entity(object):
	def __init__(self, **kwargs):
		self._entity_name = kwargs.pop('_entity_name')
		self.__dict__.update(**kwargs)
	
	def __setitem__(self, key, value):
		setattr(self, key, value)
		
	def __getitem__(self, key):
		return getattr(self, key)
	
	def __repr__(self):
		return str(self.__dict__)


class EntityManager(object):
	"""
	Joseph's entity 
	
	TODO: 
		- Entity stack
		- Doc strings
	"""
	def __init__(self, app_root, data_dir='data', file_ext='yml'):
		self.app_root = app_root
		self.data_dir = os.path.join(self.app_root, data_dir)
		self.file_ext = file_ext
		
	def _construct_from_file(self, name, entity, safe_load):
		name = '{0}.{1}'.format(name, self.file_ext)
		filename = os.path.join(self.data_dir, name)
	
		with open(filename, 'r') as file:
			if safe_load:
				payload = yaml.safe_load(file)
				
			else:
				payload = yaml.load(file)

		if isinstance(payload, dict) and len(payload) > 0:
			entity = entity(entity_name=name, **payload)
			
		else:
			raise JosephFileNotFound('File {} does not exist or is empty'.format(filename))
			
		return entity
		
	def _construct_new_entity(self, name, entity, **kwargs):
		entity = entity(name, **kwargs)
	
	def construct(self, name, entity=Entity, safe_load=True, data=None):		
		try:
			entity = self._construct_from_file(name, entity, safe_load)
			
		except FileNotFoundError:
			if not data:
				raise ValueError('Could not create entity from \'{0}\''.format(data))
		
			elif not isinstance(data, dict):
				raise ValueError('Expected dict as paramater \'data\', got {0}'.format(type(data)))
				
			entity = entity(name, data)
			self.write_to_file(entity)
		
		return entity
		
	def delete(self, entity):	
		if isinstance(entity, Entity):
			name = entity._entity_name
			
		elif isinstance(entity, str):
			name = entity
			
		else:
			raise ValueError('Unsupported type provided')

		filename = os.path.join(self.data_dir, '{0}.{1}'.format(name, self.file_ext))
		os.remove(filename)
			
	def write_to_file(self, entity):
		filename = os.path.join(self.data_dir, '{0}.{1}'.format(entity._entity_name, self.file_ext))
		
		with open(filename, 'w') as file:
			yaml.dump(entity.__dict__, file, default_flow_style=False)
