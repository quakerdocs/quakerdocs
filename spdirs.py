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
    option_spec: Dict[str, Callable[[str], Any]] = {}

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
        tocdata['maxdepth'] = self.options.get('maxdepth', -1)
        tocdata['caption'] = self.options.get('caption')
        tocdata['numbered'] = self.options.get('numbered', 0)

        wrappernode = nodes.compound(classes=['toctree-wrapper'])

        ret = self.parse_content(tocdata)
        items = list()

        # TODO: Make this recursive!
        for title, ref, children in ret:
            lst_item = nodes.list_item('', nodes.paragraph('', '', nodes.reference('', title, refuri=ref)))
            if len(children) > 0:
                blst = nodes.bullet_list()
                for c in children:
                    blst += nodes.list_item('', nodes.paragraph('', '', nodes.reference('', c, refuri=ref)))
                lst_item.append(blst)
            items.append(lst_item)
        if tocdata['numbered'] == 1:
            lst = nodes.enumerated_list()
        else:
            lst = nodes.bullet_list()
        lst.extend(items)
        wrappernode.extend([nodes.paragraph('', tocdata['caption'], classes=['caption']), lst])
        return [wrappernode]

    def parse_content(self, tocdata):
        ret = []
        for entry in self.content:
            explicit = explicit_title_re.match(entry)
            children = list()
            if (explicit):
                title, ref = explicit.group(1), explicit.group(2)
                ref = os.path.join(self.state.document.current_source, entry + ".html")
            else:
                src_dir = self.state.document.settings.src_dir
                ref = os.path.join(entry + ".html")
                src = os.path.join(src_dir, entry)
                if not src.endswith('.rst'):
                    src += '.rst'

                if os.path.exists(src):
                    doctree = docutils.core.publish_doctree(open(src, 'r').read(), settings_overrides={'src_dir': src_dir})
                else:
                    title = 'Not found'
                    continue

                # Find the page title.
                try:
                    title = next(iter(doctree.traverse(nodes.title)))
                    title = title[0].astext()
                except StopIteration:
                    title = ''

                # Find headers in document.
                if tocdata['maxdepth'] > 1:
                    for h in doctree.traverse(nodes.section):
                        children.append(h[0].astext())

            ret.append((title, ref, children))

        return ret


def setup():
    directives.register_directive('toctree', TocTree)
    directives.register_directive('only', Only)
    directives.register_directive('rst-class', Class)
    directives.register_directive('include', Include)
