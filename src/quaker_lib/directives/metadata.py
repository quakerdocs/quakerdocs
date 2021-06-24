"""Module that implements a directive to retrive metadata from a file.

This is a small directive and associated node that reads metadata from a file,
Rst or Md.

Notes
-----
The metadata variables should be of the form:
    name = value
    ...

Attributes
----------
default_fields : dictionary
    A dictionary of default values for metadata entries.
false_values : set
    A set of string values that represent a false boolean

"""

from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives

# The metadata fields and their default values.
default_fields = {'priority': 1.0,
                  'ignore': False}

# The values which are interpreted as false.
false_values = {'false', 'f', '0', 'no', 'n'}


class metadata(nodes.Inline, nodes.Element):
    """
    Class for the metadata node
    """
    def __init__(self, fields):
        """Create nodes to contain the metadata."""
        nodes.Element.__init__(self)
        for key, value in fields.items():
            setattr(self, key, value)


class MetadataDirective(Directive):
    """A directive to get the metadata from the files.

    Attributes
    ----------
    has_content : bool
        Tell docutils that this directive uses it's content.

    """

    has_content = True

    def run(self):
        """ Run method that docutils uses on directive encounter. """

        fields = default_fields.copy()

        # Get the variables on each line
        for line in self.content:
            # Split on =
            var = line.replace(' ', '').split('=')

            # Check that the syntax was used correctly.
            if len(var) != 2:
                print(f'Warning: invalid metadata: {line}')
                print(f'\t At file {self.state.document.settings.page.path}')
                continue

            name, value = var

            # Parse the value and update the field.
            try:
                # Check if the default type is a bool and parse accordingly.
                if isinstance(fields[name], bool):
                    fields[name] = value.lower() not in false_values
                # Else use the default type to cast the string.
                else:
                    fields[name] = type(fields[name])(value)
            except (ValueError, KeyError):
                print(f'Warning: invalid metadata: {line}')
                print(f'\t At file {self.state.document.settings.page.path}')

        return [metadata(fields)]


def get_metadata(doctree):
    """ Helper function to get the metadata from a doctree.

    Gets the metadata of a parsed doctree, or creates the default metadata
    if it does not exist.

    Returns
    -------
     : metadata
        The node containing the metadata

    """
    try:
        return next(iter(doctree.traverse(lambda n: isinstance(n, metadata))))
    except StopIteration:
        return metadata(default_fields)


def setup():
    """ Add the metadata directives. """
    directives.register_directive('metadata', MetadataDirective)
