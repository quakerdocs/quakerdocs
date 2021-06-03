import os
import html
import json

from docutils import io, nodes, utils
from sphinx.locale import _
from docutils.nodes import Element, Admonition
from docutils.parsers.rst import (
    Directive, states, directives, convert_directive_function
)


class IncludeJSON(Directive):
    """
    Include content read from a separate source json file.
    """

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {'path': str, 'prepend': str}

    standard_include_path = os.path.join(
        os.path.dirname(states.__file__), 'include'
    )

    def run(self):
        """Include a file as part of the content of this reST file."""
        source = self.state_machine.input_lines.source(
            self.lineno - self.state_machine.input_offset - 1
        )
        source_dir = os.path.dirname(os.path.abspath(source))
        path = directives.path(self.arguments[0])
        if path.startswith('<') and path.endswith('>'):
            path = os.path.join(self.standard_include_path, path[1:-1])
        path = os.path.normpath(os.path.join(source_dir, path))
        path = utils.relative_path(None, path)
        path = nodes.reprunicode(path)
        encoding = self.options.get(
            'encoding', self.state.document.settings.input_encoding
        )
        e_handler = self.state.document.settings.input_encoding_error_handler
        try:
            self.state.document.settings.record_dependencies.add(path)
            include_file = io.FileInput(
                source_path=path, encoding=encoding, error_handler=e_handler
            )
        except UnicodeEncodeError as error:
            raise self.severe(
                'Problems with "%s" directive path:\n'
                'Cannot encode input file path "%s" '
                '(wrong locale?).' % (self.name, path)
            )
        except IOError as error:
            raise self.severe(
                'Problems with "%s" directive path:\n%s.' % (self.name, error)
            )
        path = self.options.get('path')
        try:
            data = json.loads(include_file.read())
            for item in path.split('/'):
                data = data[item]
            assert isinstance(data, str)
        except UnicodeError as error:
            raise self.severe(
                'Problem with "%s" directive:\n%s' % (self.name, error)
            )

        if self.options.get('prepend'):
            data = f'{self.options.get("prepend")} {data}'
        self.state_machine.insert_input(data.split('\n'), path)
        return []


def setup(app):
    app.add_directive('json_include', IncludeJSON)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
