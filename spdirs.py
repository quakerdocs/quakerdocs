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


class TocTree(Directive):
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
        tocdata = {}
        tocdata['entries'] = []
        tocdata['maxdepth'] = self.options.get('maxdepth', -1)
        tocdata['caption'] = self.options.get('caption')
        tocdata['numbered'] = self.options.get('numbered', 0)
        tocdata['reversed'] = 'reversed' in self.options
        wrappernode = nodes.compound(classes=['toctree-wrapper'])

        list_type = nodes.enumerated_list if tocdata['numbered'] else nodes.bullet_list
        lst = list_type()

        self.parse_content(tocdata)
        items = TocTree.parse_entries(tocdata['entries'], tocdata['maxdepth'], list_type=list_type)

        lst.extend(items)
        wrappernode.extend([
            nodes.paragraph('', tocdata['caption'], classes=['caption']),
            lst
        ])
        return [wrappernode]

    def parse_node(node, ref):
        entries = list()
        for c in node.children:
            if not isinstance(c, nodes.section):
                continue

            if len(c.children) > 0:
                title = c.next_node(nodes.Titular)
                if title:
                    children = TocTree.parse_node(c, ref)
                    anchor = c.attributes['ids'][0]  # Use id of the anchor, not of the section!
                    entries.append((title.astext(), '%s#%s' % (ref, anchor), children))

        return entries

    # TODO: Integrate with search index?
    def parse_content(self, tocdata):
        for entry in self.content:
            children = list()
            src_dir = self.state.document.settings.src_dir
            if entry.endswith('.rst'):
                entry = entry[:-4]

            explicit_link = explicit_title_re.match(entry)
            if (explicit_link):
                title, ref = explicit_link.group(1), explicit_link.group(2)
                if not ref.startswith("https://") and not ref.startswith("http://"):
                    ref = os.path.join(src_dir, ref + ".html")
            else:
                ref = os.path.join(entry + ".html")
                src = os.path.join(src_dir, entry + ".rst")

                if os.path.exists(src):
                    doctree = docutils.core.publish_doctree(open(src, 'r').read(), settings_overrides={'src_dir': src_dir})
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

        if tocdata['reversed']:
            tocdata['entries'] = list(reversed(tocdata['entries']))

    def parse_entries(entries, depth=999, list_type=nodes.bullet_list):
        items = list()
        for title, ref, children in entries:
            lst_item = nodes.list_item('', nodes.paragraph('', '', nodes.reference('', title, refuri=ref)))
            if len(children) > 0 and depth > 1:
                # Do we want this? i.e. check plagiarism.html in ToC
                # This is similar to Sphinx
                if len(children) == 1 and len(children[0][2]) > 1:
                    children = children[0][2]
                blst = list_type()
                blst.extend(TocTree.parse_entries(children, depth=depth-1))
                lst_item.append(blst)
            items.append(lst_item)
        return items


def setup():
    directives.register_directive('toctree', TocTree)
    directives.register_directive('only', Only)
    directives.register_directive('rst-class', Class)
    directives.register_directive('include', Include)  # Does not work yet
