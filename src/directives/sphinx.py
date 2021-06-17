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


class toc_data(nodes.General, nodes.Element):
    """
    Container class for Toc data.
    """
    pass


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
        tocdata['content'] = self.content
        tocdata['src_dir'] = self.state.document.settings.src_dir
        tocdata['src_path'] = self.state.document.settings.src_path

        tocdata['entries'] = []
        tocdata['maxdepth'] = self.options.get('maxdepth', -1)
        tocdata['caption'] = self.options.get('caption')
        tocdata['numbered'] = 'numbered' in self.options
        tocdata['reversed'] = 'reversed' in self.options

        wrappernode = nodes.compound(classes=['toctree-wrapper'])
        wrappernode.append(tocdata)
        list_type = (nodes.enumerated_list if tocdata['numbered']
                     else nodes.bullet_list)
        lst = list_type()

        # Parse ToC content.
        TocTree.parse_content(tocdata)
        items = TocTree.to_nodes(tocdata['entries'], tocdata['maxdepth'],
                                 list_type=list_type)

        # Add ToC to document.
        lst.extend(items)
        if tocdata['caption'] is not None:
            wrappernode += nodes.paragraph('', tocdata['caption'],
                                           classes=['caption'])
        if len(lst) > 0:
            wrappernode += lst
        return [wrappernode]

    @staticmethod
    def parse_node(node, ref):
        """
        Generate a tree-like structure for the sections in a given doctree.
        """
        entries = []

        # Iterate over all section-nodes belonging to node.
        for child in node.children:
            if not isinstance(child, nodes.section):
                continue

            # Only continue if the current section contains a title.
            if len(child.children) > 0:
                title = child.next_node(nodes.Titular)
                if title:
                    children = TocTree.parse_node(child, ref)
                    # Use id of the anchor, not of the section!
                    anchor = child.attributes['ids'][0]
                    entries.append((title.astext(), '%s#%s'
                                    % (ref, anchor), children))

        return entries

    # TODO: Integrate with search index?
    @staticmethod
    def parse_content(tocdata: toc_data):
        """
        Fill the toctree data structure with entries.
        """
        for entry in tocdata['content']:
            children = []
            src_dir = tocdata['src_dir']
            if entry.endswith('.rst'):
                entry = entry[:-4]

            # Check if current entry is in format 'Some Title <some_link>'.
            explicit_link = util.link_explicit(entry)

            if explicit_link is not None:
                title, ref = explicit_link
                if (not ref.startswith("https://")
                        and not ref.startswith("http://")):

                    if not ref.startswith('/'):
                        ref = tocdata['src_path'].parent / ref

                    ref = Path(ref).with_suffix('.html')
            else:
                ref = os.path.join(entry + ".html")
                src = os.path.join(src_dir, entry + ".rst")

                if not os.path.exists(src):
                    continue

                doctree = docutils.core.publish_doctree(
                    Path(src).read_text(),
                    source_path=src,
                    settings_overrides={
                        'src_dir': src[:-4],
                        'src_path': (tocdata['src_path'] / entry).parent
                    }
                )

                # Find the page title.
                try:
                    title = next(iter(doctree.traverse(nodes.title)))
                    title = title[0].astext()
                except StopIteration:
                    title = 'Not found'

                # Find section headers in document.
                children = TocTree.parse_node(doctree, ref)

            tocdata['entries'].append((title, ref, children))

        # Reverse if required.
        if tocdata['reversed']:
            tocdata['entries'] = list(reversed(tocdata['entries']))

    @staticmethod
    def to_nodes(entries, depth=999, list_type=nodes.bullet_list):
        """
        Convert a given ToC-tree into a displayable structure for the document.
        """
        items = []
        for title, ref, children in entries:
            lst_item = nodes.list_item('', nodes.paragraph('', '',
                                       nodes.reference('', title, refuri=ref)))

            # Parse children, but only if maxdepth is not yet reached.
            if len(children) > 0 and depth > 1:
                # Do we want to collapse some entries? i.e. plagiarism.html
                # This is similar to Sphinx
                while len(children) == 1 and len(children[0][2]) > 1:
                    children = children[0][2]
                blst = list_type()
                blst.extend(TocTree.to_nodes(children, depth=depth-1,
                                             list_type=list_type))
                lst_item.append(blst)
            items.append(lst_item)
        return items

    @staticmethod
    def to_html(tocdata: toc_data):
        """
        Parse the TocData data-structure to HTML.
        """
        ret = ('<p class="caption menu-label"><span class="caption-text">'
               '{%s}</span></p>' % tocdata['caption'])
        ret += TocTree.entries_to_html(tocdata['entries'])
        return ret

    @staticmethod
    def entries_to_html(entries: Iterable, depth=999, begin_depth=0):
        """
        Parse the entries that need to be in the ToC to HTML format.
        """
        # TODO: Fix indentation
        add_class = '' if begin_depth == 0 else 'is-collapsed'
        ret = f'<ul class="menu-list {add_class}">\n'
        for title, ref, children in entries:
            lst_item = '<li><span class="level mb-0"><a '

            if '#' in ref:
                lst_item += f'onClick="expandSidebar(\'{ref}\')" '

            lst_item += f'href={ref}>{title}</a>'

            if len(children) > 0:
                lst_item += ('<span onclick="toggleExpand(this.parentNode)" '
                             'class="is-clickable icon is-small level-right">'
                             '<i class="fa arrow-icon fa-angle-right" '
                             'aria-hidden="true"></i></span>')

            lst_item += '</span>'

            # Parse children, but only if maxdepth is not yet reached.
            if len(children) > 0 and depth > 1:
                # Do we want to collapse some entries? i.e. plagiarism.html
                # This is similar to Sphinx
                while len(children) == 1 and len(children[0][2]) > 1:
                    children = children[0][2]
                blst = TocTree.entries_to_html(children, depth=depth-1,
                                               begin_depth=begin_depth+1)
                lst_item += blst
            lst_item += "</li>\n"
            ret += lst_item
        ret += "</ul>"
        return ret


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


class ref_element(nodes.General, nodes.Element):
    """
    Custom reference node to handle unparsed pages.
    """
    pass


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
    node['ref'] = ref.replace('_', '-').lower()

    return [node], []


class kbd_element(nodes.General, nodes.Element):
    """
    Empty node for rendering keyboard inputs
    """
    pass


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
