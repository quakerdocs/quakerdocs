"""
Metadata directive used to embed metadata in a RST file.
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
    """
    Get the metadata from the files.
    """

    has_content = True

    def run(self):
        fields = default_fields.copy()

        for line in self.content:
            var = line.replace(' ', '').split('=')
            if len(var) != 2:
                # TODO: print file name
                print(f'Warning: invalid metadata: {line}')
                continue

            name, value = var

            # Parse the value and update the field.
            try:
                if isinstance(fields[name], bool):
                    fields[name] = value.lower() not in false_values
                else:
                    fields[name] = type(fields[name])(value)
            except (ValueError or KeyError):
                # TODO: print filename.
                print(f'Warning: invalid metadata: {line}')

        return [metadata(fields)]


def get_metadata(doctree):
    """Get the metadata of a parsed doctree, or create the default metadata
    if it does not exist.
    """
    try:
        return next(iter(doctree.traverse(lambda n: isinstance(n, metadata))))
    except StopIteration:
        return metadata(default_fields)


def setup():
    """Add the metadata directives.
    """
    directives.register_directive('metadata', MetadataDirective)
