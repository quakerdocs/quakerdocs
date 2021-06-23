"""
Implement directives used by Sphinx

All implementations of the directives have been inspired by:
https://github.com/sphinx-doc/sphinx/blob/9e1b4a8f1678e26670d3
4765e74edf3a3be3c62c/sphinx/directives/other.py
"""

import os.path
from typing import Iterable
import docutils.core
from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives, roles
from docutils.parsers.rst.roles import set_classes
from docutils.parsers.rst.directives.misc import Class, Include

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

from pathlib import Path
import util


class kbd_element(nodes.General, nodes.Element):
    """
    Empty node for rendering keyboard inputs
    """
    pass


class toc_data(nodes.General, nodes.Element):
    """
    Container class for Toc data.
    """
    pass


class ref_element(nodes.General, nodes.Element):
    """
    Custom reference node to handle unparsed pages.
    """
    pass


class Only(Directive):
    """
    Directive for only including content for certain builds.
    """
    required_arguments = 1
    optional_arguments = 1

    has_content = True
    option_spec = {}

    def run(self):
        """
        Create nodes for this directive.
        """
        node = nodes.container()

        if (self.arguments[0] == 'html'
           or (self.arguments[0] == 'not' and self.arguments[1] != 'html')):
            self.state.nested_parse(self.content, self.content_offset, node,
                                    match_titles=True)
            return [*node]

        return []


class TocTree(Directive):
    """
    Directive for generating a Table of Contents
    """
    has_content = True

    option_spec = {
        'maxdepth': int,
        'name': directives.unchanged,
        'caption': directives.unchanged_required,
        'glob': directives.flag,
        'hidden': directives.flag,
        'includehidden': directives.flag,
        'numbered': directives.flag,
        'titlesonly': directives.flag,
        'reversed': directives.flag,
    }

    def run(self):
        """
        Code that is being run for the directive.
        """
        tocdata = toc_data()
        tocdata['maxdepth'] = self.options.get('maxdepth', -1)
        tocdata['caption'] = self.options.get('caption')
        tocdata['reversed'] = 'reversed' in self.options
        tocdata['type'] = (nodes.enumerated_list if 'numbered' in self.options
                            else nodes.bullet_list)()

        self.main = self.state.document.settings.main
        self.page = self.state.document.settings.page

        tocdata['entries'] = self.parse_content()


        return [tocdata]

    def parse_content(self):
        """
        Fill the toctree data structure with entries.
        """
        result = []
        for entry in self.content:
            # Check if current entry is in format 'Some Title <some_link>'.
            explicit_link = util.link_explicit(entry)

            if explicit_link:
                title, ref = explicit_link
            else:
                title = None
                ref = entry
            result.append((title, ref))
            self.page.use_reference(ref)
        return result


class CodeBlock(Directive):
    """
    Directive for displaying code samples.
    """
    option_spec = {
        'name': directives.unchanged,
        'linenos': directives.flag,
        'lineno-start': int,
        'caption': directives.unchanged_required
    }

    has_content = True
    optional_arguments = 1

    def run(self):
        """
        Create nodes for this directive.
        """
        language = self.arguments[0] if len(self.arguments) > 0 else None
        linenos = 'linenos' in self.options
        linenostart = self.options.get('lineno-start', 1)
        caption = self.options.get('caption', '')
        code = "\n".join(self.content)

        formatter = HtmlFormatter(linenos=linenos, linenostart=linenostart)
        if language is not None:
            lexer = get_lexer_by_name(language, stripall=True)
            code = highlight(code, lexer, formatter)
        else:
            code = '<div class="highlight"><pre>%s</pre></div>' % code

        wrappernode = nodes.compound(classes=[f"highlight {language}"])
        wrappernode.append(nodes.raw('', code, format="html"))
        wrappernode.append(nodes.paragraph('', caption))

        return [wrappernode]


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

    title, ref = explicit_link
    set_classes(options)

    node = ref_element()
    node['title'] = title
    node['ref'] = ref
    self.state.document.settings.page.use_reference(ref)

    return [node], []


def kbd_role(role, rawtext, text, lineno, inliner, options={}, content=[]):
    """
    Role for displaying keyboard inputs.
    """
    set_classes(options)
    node = kbd_element()
    node['keys'] = text.split('+')
    return [node], []


def setup():
    """
    Setup function for this 'extension'
    """
    directives.register_directive('only', Only)
    directives.register_directive('rst-class', Class)
    directives.register_directive('include', Include)  # Does not work yet
    directives.register_directive('toctree', TocTree)
    directives.register_directive('code-block', CodeBlock)

    roles.register_canonical_role('ref', ref_role)
    roles.register_canonical_role('kbd', kbd_role)
