"""
Implement directives used in the CodeGrade reStructuredText.
"""

from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives
from urllib.parse import urlparse


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


class iframe_node(nodes.General, nodes.Element):
    """
    Container class for IFrameDirective.
    """
    ...


class IFrameDirective(Directive):
    """
    Directive for HTML iframes.
    """
    option_spec = {
        'width': int,
        'height': int
    }

    required_arguments = 1
    optional_arguments = 2

    def run(self):
        if self.arguments:
            url = self.arguments[0]
            node = iframe_node()
            xy_ratio = 3/5

            if self.options:
                width = self.options[0]
                height = self.options[1] if len(self.options) > 1 else \
                    width * xy_ratio
            else:
                width = 500
                height = width * xy_ratio

            node['url'] = url
            node['width'] = int(width)
            node['height'] = int(height)

        return [node]


def setup():
    directives.register_directive('example', ExampleDirective)
    directives.register_directive('iframe', IFrameDirective)
