"""
Implement directives used in the CodeGrade reStructuredText.
"""

from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives, roles
from docutils.parsers.rst.roles import set_classes
from docutils import utils

import util


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


def ref_role(role, rawtext, text, lineno, inliner, options={}, content=[]):
    """
    Role for creating hyperlink to other documents.
    """
    explicit_link = util.link_explicit(text)
    if explicit_link is None:
        msg = inliner.reporter.error(
            'Link %s in invalid format; '
            'must be "Some Title <some_link_label>"' % text, line=lineno)
        prb = inliner.problematic(rawtext, rawtext, msg)
        return [prb], [msg]

    # TODO: Fix link path, use search index?
    title, ref = explicit_link
    set_classes(options)
    node = nodes.reference(rawtext, title, refuri=ref, **options)
    return [node], []


def setup():
    directives.register_directive('deprecation_note', DeprecationNote)
    directives.register_directive('warning', WarningDirective)
    directives.register_directive('example', ExampleDirective)

    roles.register_canonical_role('ref', ref_role)
