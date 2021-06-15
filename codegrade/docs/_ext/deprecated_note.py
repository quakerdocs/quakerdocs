import os
import html
import json

from docutils import io, nodes, utils
from docutils.nodes import Element, Admonition
from docutils.parsers.rst import (
    Directive, states, directives, convert_directive_function
)

TEMPLATE = """
.. tip::

   CodeGrade has a Help Center, with better guides, more videos and updated
   documentation. The documentation and guides on this website are deprecated
   and will not be updated in the future. Please `click here
   <{new_url}>`__ to go to this page on the Help Center!
""".strip()


class DeprecatedNote(Directive):
    """
    Include content read from a separate source json file.
    """

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True

    standard_include_path = os.path.join(
        os.path.dirname(states.__file__), 'include'
    )

    def run(self):
        """Include a file as part of the content of this reST file."""
        new_path = self.arguments[0].lstrip('/')
        new_url = 'https://help.codegrade.com/{}'.format(new_path)
        data = TEMPLATE.format(new_url=new_url)
        self.state_machine.insert_input(data.splitlines(), data)
        return []


def setup(app):
    app.add_directive('deprecation_note', DeprecatedNote)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
