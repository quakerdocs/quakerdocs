"""
Functionality related to the application.
"""

from types import SimpleNamespace
from importlib import import_module
# from docutils import nodes
from docutils.parsers.rst import directives, roles


class SphinxApp:
    """
    Class to emulate a Sphinx app for using extensions.
    """
    def __init__(self):
        # Ignore for now
        self.config = SimpleNamespace()
        self.handlers = {
            'html': [],
            'latex': [],
            'text': []
        }

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


def setup_extension(extension, app):
    """
    Load extension module, and call the containing setup function
    """
    mod = import_module(extension)
    setup = getattr(mod, 'setup')
    setup(app)
