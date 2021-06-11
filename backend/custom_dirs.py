"""
Implement directives used in the CodeGrade reStructuredText.
"""

from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives


class ExampleDirective(Directive):
    has_content = True
    optional_arguments = 100

    def run(self):
        wrapper = nodes.admonition('', classes=['example'])
        title = "Example"
        # Add title to example text if it is supplied.
        if len(self.arguments) > 0:
            title += ": " + ' '.join(self.arguments)

        wrapper.append(nodes.paragraph('', title, classes=['example-title']))

        # Content
        content_wrapper = nodes.compound(classes=['example-content'])
        wrapper.append(content_wrapper)

        self.state.nested_parse(
            self.content, self.content_offset, content_wrapper
        )

        return [wrapper]


def setup():
    directives.register_directive('example', ExampleDirective)
