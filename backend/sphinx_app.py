"""
Functionality to emulate a Sphinx app for using extensions
"""

import optparse
from importlib import import_module
from docutils.parsers.rst import directives, roles


class SphinxApp:
    def __init__(self):
        # Ignore for now
        self.config = optparse.Values()

    def add_directive(self, name, directive):
        directives.register_directive(name, directive)

    def add_role(self, name, role):
        roles.register_local_role(name, role)


def setup_extension(extension, app):
    """
    Load extension module, and call the containing setup function
    """
    mod = import_module(extension)
    setup = getattr(mod, 'setup')
    setup(app)
