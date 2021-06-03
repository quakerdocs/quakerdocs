"""
Implement directives used in the CodeGrade reStructuredText.
"""

from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives


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
        return [nodes.tip('', nodes.paragraph('', '', *text))]


def setup():
    directives.register_directive('deprecation_note', DeprecationNote)
