from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives

default_fields = {'priority': 1.0,
                  'ignore': False}

false_values = {'false', 'f', '0', 'no', 'n'}

class metadata(nodes.Inline, nodes.Element):
    def __init__(self, fields):
        nodes.Element.__init__(self)
        for key, value in fields.items():
            setattr(self, key, value)


class MetadataDirective(Directive):
    has_content = True

    def run(self):
        fields = default_fields.copy()

        for line in self.content:
            var = line.replace(' ', '').split('=')
            if len(var) != 2:
                print(f'Warning: invalid metadata: {line}') # TODO: print file name
                continue

            # Check if the metadata field exists.
            name, value = var

            # Parse the value.
            try:
                if type(fields[name]) == bool:
                    fields[name] = value.lower() not in false_values
                else:
                    fields[name] = type(fields[name])(value)
            except ValueError or KeyError:
                print(f'Warning: invalid metadata: {line}')

        return [metadata(fields)]


def get_metadata(doctree):
    """ TODO """
    try:
        return next(iter(doctree.traverse(lambda n: isinstance(n, metadata))))
    except StopIteration:
        return metadata(default_fields)


def setup():
    directives.register_directive('metadata', MetadataDirective)
