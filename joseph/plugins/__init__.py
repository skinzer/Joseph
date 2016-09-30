import os
import types

from ..entities import EntityManager
from ..entities.types import PluginType
from ..helpers import Stack


class PluginManager(object):
    """
    Joseph's PluginManager

    At the moment capable of discovering files
    with a predefined file extension. The discovered files
    are stored as an entity in the :class:`EntityManager`.
    """

    def __init__(self, app_root, plugin_dir='plugins', file_ext='py'):
        self.app_root = app_root
        self.file_ext = file_ext
        self.not_run = Stack()
        self.plugin_dir = os.path.join(app_root, plugin_dir)

    def discover(self, auto_compile=True, auto_run=True):
        """
        Finds all files in the given directory with a file extension
        that matches :property:`file_ext`.

        If :param:`auto_compile` is ``True``, the :meth:`compile` is
        called on the plugin, otherwise a plugin entity is yielded.
        """
        for file in os.listdir(self.plugin_dir):
            if file.endswith(self.file_ext):
                filename = file.replace(self.file_ext, '')
                plugin_entity = entity_manager.construct(filename, PluginType)

                if auto_compile:
                    self.compile(plugin_entity, auto_run)

                else:
                    yield plugin_entity

    def compile(self, plugin_entity, auto_run=True):
        """
        Compiles and executes the plugin belonging to the entity.
        If :param:`auto_run` is set to ``False``, the compiled
        module is stored on then the entity's :property:`compiled`

        :param plugin_entity: Entity representing the plugin constructed
                              by the entity manager
        :param auto_run:

        """
        filename = os.path.join(self.plugin_dir, plugin_entity.name)

        plugin_type = types.ModuleType('plugin')
        plugin_type.__file__ = filename

        with open(filename, 'r') as file:
            exec(compile(file.read(), filename, 'exec'), plugin_type.__dict__)

        if auto_run:
            plugin_type.run()

        else:
            entity_manager.update(plugin_entity, compiled=plugin_type)

    def compile_all(self, auto_run=True):
        """
        Compiles all plugins stored in `self.discovered`
        if the :param:`auto_run` is set to ``True`` the plugin's
        :func:`run` will be called after compiling otherwise a
        generator object is yielded which compiles the plugin
        on request.

        :param auto_run: True / False
        :yield: Compiled plugin
        """
        for plugin_entity in self.discovered:
            if auto_run:
                self.compile(plugin_entity, auto_run=True)

            else:
                yield self.compile(plugin_entity, auto_run=False)
