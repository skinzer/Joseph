import os
import types

from config import APP_ROOT


class Config(dict):
    """
    Joseph's config object, which works like a regular dictionary, but has
    a few tricks up its sleeve.

    A config file will be loaded as if it was a regular module. The variables
    will be evaluated and used to update the config object.

    Config values can be accessed with the corresponding dictionary key or by
    using the key as a property.

    Ex:
        print(config[KEY])
        print(config.KEY)


    """
    DEFAULT_CONFIG = {

    }

    def __init__(self, *args, **kwargs):
        """
        Initializes the config object. The :param kwargs: can be used to pass
        default values as a `dictionary`, if no values are provided, the
        object's default values are used.

        :param args: Default values as dict
        :param kwargs: Default values
        """
        super(dict, self).__init__()

        for arg in args:
            if isinstance(arg, dict):
                self.update(arg)

        self.update(**kwargs or self.DEFAULT_CONFIG)

    def __setattr__(self, key, value):
        """
        This method makes it possible to set the dict key like you would
        with any other object. This an the :meth:`__getitem__` are
        implemented solely for convenience.

        :param key: Key to update
        :param value: Value to set to :param key:
        """
        self[key] = value

    def __getattr__(self, item):
        """
        This method makes it possible to get the dict key like you would
        with any other object. This an the :meth:`__setitem__` are
        implemented solely for convenience.

        :param item: Item you want to get
        :return: Value to the requested item
        """
        return self[item]

    def items(self):
        """ Make sure not to return private attributes """
        return {key: value for key, value in dict.items(self) if key.isupper()}

    @property
    def proxy(self):
        """
        By using the :propery:`proxy` you get a ``MappingProxyType`` which
        is a readonly copy of `self`

        :return: ``MappingProxyType`` of self
        """
        return types.MappingProxyType(self)

    async def from_file(self, filename='config.py', silent=False):
        """
        This method imports a file as if it was a 'normal' module and updates
        itself with the variables

        This method is inspired by Flask which handles it config the same way

        :param filename: The relative or absolute path to the config file
        :param silent: Set to ``True`` if you do not want any errors to show
        :return: ``MappedProxyType``
        """
        filename = os.path.join(APP_ROOT, filename)

        config = types.ModuleType('config')
        config.__file__ = filename

        try:
            with open(filename, 'r') as file:
                exec(compile(file.read(), filename, 'exec'), config.__dict__)

        except IOError as e:
            if not silent:
                raise JosephConfigException(e.strerror)

        for key in dir(config):
            if key.isupper():
                self[key] = getattr(config, key)

        return self.proxy

    async def from_env_vars(self, prefix="JOSEPH_"):
        """ Allows reading config variables from environment variables """
        for key, value in os.environ.items():
            if key.startswith(prefix):
                key = key.replace(prefix)

                self[key] = value

    def __repr__(self):
        return str(self.items())
