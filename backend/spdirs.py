"""
Implement directives used by Sphinx

All implementations of the directives have been inspired by:
https://github.com/sphinx-doc/sphinx/blob/9e1b4a8f1678e26670d34765e74edf3a3be3c62c/sphinx/directives/other.py
"""

import re
import os.path
from typing import Any, Callable, Dict

import docutils.core
from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives.misc import Class, Include
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

explicit_title_re = re.compile(r'^(.+?)\s*(?<!\x00)<([^<]*?)>$', re.DOTALL)


class Only(Directive):
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True  # necessary?

    has_content = True
    option_spec = {}

    def run(self):
        node = nodes.container()

        if self.arguments[0] == 'html' or (self.arguments[0][:4] == 'not ' and self.arguments[0][4:] != 'html'):  # FIX
            self.state.nested_parse(self.content, self.content_offset, node, match_titles=True)
            return [*node]

        return []


def int_or_nothing(argument: str) -> int:
    if not argument:
        return 999
    return int(argument)


class TocData(nodes.General, nodes.Element):
    """
    Container class for Toc data.
    """
    ...


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
        'numbered': int_or_nothing,
        'titlesonly': directives.flag,
        'reversed': directives.flag,
    }

    def run(self):
        """
        Code that is being run for the directive.
        """
        tocdata = TocData()
        tocdata['content'] = self.content
        tocdata['src_dir'] = self.state.document.settings.src_dir

        tocdata['entries'] = []
        tocdata['maxdepth'] = self.options.get('maxdepth', -1)
        tocdata['caption'] = self.options.get('caption')
        tocdata['numbered'] = self.options.get('numbered', 0)
        tocdata['reversed'] = 'reversed' in self.options

        wrappernode = nodes.compound(classes=['toctree-wrapper'])
        wrappernode.append(tocdata)
        list_type = nodes.enumerated_list if tocdata['numbered'] else nodes.bullet_list
        lst = list_type()

        # Parse ToC content.
        TocTree.parse_content(tocdata)
        items = TocTree.to_nodes(tocdata['entries'], tocdata['maxdepth'], list_type=list_type)

        # Add ToC to document.
        lst.extend(items)
        if tocdata['caption'] is not None:
            wrappernode += nodes.paragraph('', tocdata['caption'], classes=['caption'])
        if len(lst) > 0:
            wrappernode += lst
        return [wrappernode]

    def parse_node(node, ref):
        """
        Generate a tree-like structure for the sections in a given doctree.
        """
        entries = list()

        # Iterate over all section-nodes belonging to node.
        for c in node.children:
            if not isinstance(c, nodes.section):
                continue

            # Only continue if the current section contains a title.
            if len(c.children) > 0:
                title = c.next_node(nodes.Titular)
                if title:
                    children = TocTree.parse_node(c, ref)
                    anchor = c.attributes['ids'][0]  # Use id of the anchor, not of the section!
                    entries.append((title.astext(), '%s#%s' % (ref, anchor), children))

        return entries

    # TODO: Integrate with search index?
    def parse_content(tocdata):
        """
        Fill the toctree data structure with entries.
        """
        for entry in tocdata['content']:
            children = list()
            src_dir = tocdata['src_dir']
            if entry.endswith('.rst'):
                entry = entry[:-4]

            # Check if current entry is in format 'Some Title <some_link>'.
            explicit_link = explicit_title_re.match(entry)
            if (explicit_link):
                title, ref = explicit_link.group(1), explicit_link.group(2)
                if not ref.startswith("https://") and not ref.startswith("http://"):
                    ref = os.path.join(src_dir, ref + ".html")
            else:
                ref = os.path.join(entry + ".html")
                src = os.path.join(src_dir, entry + ".rst")

                if os.path.exists(src):
                    doctree = docutils.core.publish_doctree(
                        open(src, 'r').read(),
                        source_path=src,
                        settings_overrides={'src_dir': src[:-4]})
                else:
                    continue

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

    def to_nodes(entries, depth=999, list_type=nodes.bullet_list):
        """
        Convert a given ToC-tree into a displayable structure for the document.
        """
        items = list()
        for title, ref, children in entries:
            lst_item = nodes.list_item('', nodes.paragraph('', '', nodes.reference('', title, refuri=ref)))

            # Parse children, but only if maxdepth is not yet reached.
            if len(children) > 0 and depth > 1:
                # Do we want to collapse some entries? i.e. plagiarism.html
                # This is similar to Sphinx
                while len(children) == 1 and len(children[0][2]) > 1:
                    children = children[0][2]
                blst = list_type()
                blst.extend(TocTree.to_nodes(children, depth=depth-1, list_type=list_type))
                lst_item.append(blst)
            items.append(lst_item)
        return items

    def to_html(tocdata):
        """
        Parse the TocData data-structure to HTML.
        """
        ret = '<p class="caption menu-label"><span class="caption-text">%s</span></p>' % tocdata['caption']
        ret += TocTree.entries_to_html(tocdata['entries'], 999)
        return ret

    def entries_to_html(entries, depth=999, begin_depth=0):
        """
        Parse the entries that need to be in the ToC to HTML format.
        """
        # TODO: Fix indentation
        add_class = '' if begin_depth == 0 else 'is-collapsed'
        ret = '<ul class="menu-list %s">\n' % add_class
        for title, ref, children in entries:
            lst_item = '<li><span class="level mb-0">\
                <a href=%s>%s</a>' % (ref, title)

            if len(children) > 0:
                lst_item += '<span onclick="toggleExpand(this)" class="is-clickable icon is-small level-right">\
                    <i class="fa arrow-icon fa-angle-right" aria-hidden="true"></i></span>'

            lst_item += '</span>'

            # Parse children, but only if maxdepth is not yet reached.
            if len(children) > 0 and depth > 1:
                # Do we want to collapse some entries? i.e. plagiarism.html
                # This is similar to Sphinx
                while len(children) == 1 and len(children[0][2]) > 1:
                    children = children[0][2]
                blst = TocTree.entries_to_html(children, depth=depth-1, begin_depth=begin_depth+1)
                lst_item += blst
            lst_item += "</li>\n"
            ret += lst_item
        ret += "</ul>"
        return ret


class CodeBlock(Directive):
    option_spec = {
        'name' : directives.unchanged,
        'linenos': directives.flag,
        'lineno-start': int,
        'caption': directives.unchanged_required
    }

    has_content = True
    optional_arguments = 100
    required_arguments = 1

    def run(self):
        language = self.arguments[0]
        lexer = get_lexer_by_name(language, stripall=True)
        linenos='linenos' in self.options
        linenostart = self.options.get('lineno-start', 1)
        caption = self.options.get('caption', '')

        formatter = HtmlFormatter(linenos = linenos, linenostart = linenostart)
        text = "\n".join(self.content)
        code = highlight(text, lexer, formatter)

        wrappernode = nodes.compound(classes=[f"highlight {language}"])
        wrappernode.append(nodes.raw('', code, format="html"))
        wrappernode.append(nodes.paragraph('', caption))

        return [wrappernode]


def setup():
    """
    Setup function for this 'extension'
    """
    directives.register_directive('only', Only)
    directives.register_directive('rst-class', Class)
    directives.register_directive('include', Include)  # Does not work yet
    directives.register_directive('toctree', TocTree)
    directives.register_directive('code-block', CodeBlock)

