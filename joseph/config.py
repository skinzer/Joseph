import os
import types

from config import APP_ROOT
from .exceptions import ConfigException


class Config(dict, object):
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

    def __init__(self, *args, **kwargs) -> None:
        """
        Initializes the config object. The :param kwargs: can be used to pass
        default values as a `dictionary`, if no values are provided, the
        object's default values are used.

        :param args: Default values as dict
        :param kwargs: Default values
        """
        super(Config, self).__init__()

        for arg in args:
            if isinstance(arg, dict):
                self.update(arg)

        self.update(**kwargs or self.DEFAULT_CONFIG)

    def __setitem__(self, key: str, value) -> None:
        """

        :param key: Config key
        :param value: Config value to be set
        :raise ConfigException: If provided key is lowercase
        """
        if not key.isupper():
            raise ConfigException("Config keys should be uppercase, got '{}' instead".format(key))
        else:
            dict.__setitem__(self, key, value)

    def __setattr__(self, key: str, value) -> None:
        """
        Sets attributes on the config object, if a lowercase key is provided
        it's assumed to be private key and therefore set as an attribute.
        Otherwise it's passed to the :meth: __setitem__

        :param key: Key to update
        :param value: Value to set to :param key:
        """
        if key.islower():
            object.__setattr__(self, key, value)
        else:
            self[key] = value

    def __getattr__(self, key: str):
        """
        Makes it possible to access config values as if they were regular
        attributes instead of a dict like.
        If a lowercase :param: `key` is provided, it's assumed to be a
        private attribute and therefore the :meth: getattribute is used.

        :param key: Key of the item
        :raise AttributeError:
        :raise KeyError:
        """
        if key.islower():
            item = object.__getattribute__(self, key)
        else:
            item = self[key]

        return item

    def keys(self) -> list:
        """ Only return non private attributes as key """
        return [key for key in dict.keys(self) if key.isupper()]

    def values(self) -> list:
        """ Make sure not to return values associated with private attributes """
        return [value for key, value in dict.items(self) if key.isupper()]

    def items(self) -> dict:
        """ Make sure not to return private attributes """
        return {key: value for key, value in dict.items(self) if key.isupper()}

    def __dir__(self) -> list:
        """ Returns everything that's not a config item """
        return [key for key in dict.__dir__(self) if not key.isupper()]

    @property
    def proxy(self) -> types.MappingProxyType:
        """ Return a readonly copy of self """
        return types.MappingProxyType(self.items())

    async def from_file(self, filename: str = 'config.py', silent: bool = False) -> types.MappingProxyType:
        """
        This method imports a file as if it was a 'normal' module and updates
        itself with the variables

        This method is inspired by Flask which handles it config the same way

        :param filename: The relative or absolute path to the config file
        :param silent: Set to ``True`` if you do not want any errors to show
        """
        filename = os.path.join(APP_ROOT, filename)

        config = types.ModuleType('config')
        config.__file__ = filename

        try:
            with open(filename, 'r') as file:
                exec(compile(file.read(), filename, 'exec'), config.__dict__)

        except IOError as e:
            if not silent:
                raise ConfigException(e.strerror)

        for key in dir(config):
            if key.isupper():
                self[key] = getattr(config, key)

        return self.proxy

    async def from_env_vars(self, prefix: str = "JOSEPH_") -> types.MappingProxyType:
        """
        Loops over environment variables and updates ``self`` with any values matching the
        specified prefix
        """
        for key, value in os.environ.items():
            if key.startswith(prefix):
                key = key.replace(prefix, '')

                self[key] = value

        return self.proxy

    def __repr__(self) -> str:
        return str(self.items())
