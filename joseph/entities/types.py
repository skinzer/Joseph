import re
import os


class Entity(object):
    """
	Represents the Joseph's base Entity

	Direct access to this class is probably not necessary
	as :class:`EntityManager` provides methods to create
	entities. However :class:`EntityManager` does not yet
	care whether it created the entity or the entity was
	created elsewhere.
	"""
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.__dict__.update(**kwargs['data'])

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        if hasattr(self, key):
            return getattr(self, key)

        else:
            raise KeyError()

    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__, str(self.__dict__))

    @property
    def entity_type(self):
        """
		Provides easy access to the entity's class name which is
		used to distinguish entities

        Converts the entity_type to snake_case using a regex for readability

		:return: Entity class name
		"""

        s = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', self.__class__.__name__)
        return re.sub('([a-z0-9])(A-Z)', r'\1_\2', s).lower()

    @property
    def filename(self):
        """
        Returns the full filename relative to the manager's `data_dir`

        :return: Relative filename
        """
        if self.entity_type != 'entity':
            filename = os.path.join(self.entity_type, self.name)

        else:
            filename = self.name

        return filename

class PluginType(Entity):
    def __init__(self):
        super(Entity, self).__init__()
        self.enabled = True

    @property
    def compiled(self):
        return self._compiled

    @compiled.setter
    def compiled(self, value):
        self._compiled = value
