"""
Functionality related to the application.
"""

from importlib import import_module
from docutils.parsers.rst import directives, roles

from quaker_lib.util import Config


class SphinxApp:
    """
    Class to emulate a Sphinx app for using extensions.
    """
    def __init__(self):
        # Ignore for now
        self.env = Config()
        self.config = Config()
        self.callbacks = {}
        self.handlers = {
            'html': [],
            'latex': [],
            'text': []
        }

        self.source_suffix = {}
        self.source_parsers = {}

    def get_handlers(self):
        """
        Return list of handlers that should be added to the translator.
        """
        return self.handlers

    def add_directive(self, name, directive):
        """
        Add a docutils directive to the program.
        """
        directives.register_directive(name, directive)

    def add_role(self, name, role):
        """
        Add a docutils role to the program.
        """
        roles.register_local_role(name, role)

    def add_node(self, node, **kwargs):
        """
        Placeholder function for adding node types to docutils.
        Does nothing at the moment.
        """
        ...

    def add_source_suffix(self, file_ext, file_type):
        """
        Add a source suffix to the project.
        """
        self.source_suffix.update({file_ext: file_type})

    def add_source_parser(self, parser):
        """
        Add a source parser to the project.
        """
        for file_ext, file_type in self.source_suffix.items():
            if file_type in parser.supported:
                self.source_parsers.update({file_ext: parser})
                return

    def add_post_transform(self, post_transform):
        """
        Add a post transform to the project.
        """
        ...

    def add_config_value(self, name, value, map):
        """
        Add a config value to the project.
        """
        self.config[name] = value

    def connect(self, event, callback):
        """
        Add an event callback to the project.
        """
        if event not in self.callbacks:
            self.callbacks[event] = []
        self.callbacks[event].append(callback)


def setup_extension(extension, app):
    """
    Load extension module, and call the containing setup function
    """
    mod = import_module(extension)
    setup = getattr(mod, 'setup')
    setup(app)
