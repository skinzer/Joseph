import os
import re

from ..states import State


class EntityType(object):
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


class ApplicationEntity(EntityType):
    """ Mixin class for in-app objects such as Joseph's core and Plugins """

    def __init__(self, *args, **kwargs):
        super(ApplicationEntity, self).__init__(*args, **kwargs)
        self.state = State(None)

    def is_running(self):
        """ Return if object is running """
        return self.state in ('STARTING', 'RUNNING')

    def is_stopped(self):
        """ Return if object is stopped """
        return self.state in ('STOPPING', 'STOPPED')

    def is_state_changing(self):
        """ Return if object is about to change states """
        return self.state in ('STARTING', 'STOPPING')
