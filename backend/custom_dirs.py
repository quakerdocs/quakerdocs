"""
Implement directives used in the CodeGrade reStructuredText.
"""

from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives, roles


class DeprecationNote(Directive):
    has_content = True
    required_arguments = 1

    def run(self):
        path = 'https://help.codegrade.com' + self.arguments[0]  # Not os.path.join()!
        text = []
        text.extend([
            nodes.Text('CodeGrade has a Help Center, with better guides, more videos and updated documentation. The documentation and guides on this website are deprecated and will not be updated in the future. Please click '),
            nodes.reference('', 'here', refuri=path),
            nodes.Text(' to go to this page on the Help Center!')
        ])
        # return [nodes.tip('', nodes.paragraph('', '', *text))]
        return []


class WarningDirective(Directive):
    has_content = True

    def run(self):
        adm = nodes.admonition('',
                               nodes.paragraph('', ' '.join(self.content)),
                               classes=['warning'])
        title = nodes.title('', 'Warning')
        adm.insert(0, title)
        return [adm]


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
    directives.register_directive('deprecation_note', DeprecationNote)
    directives.register_directive('warning', WarningDirective)
    directives.register_directive('example', ExampleDirective)
