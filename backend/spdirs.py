"""
Implement directives used by Sphinx

All implementations of the directives have been inspired by:
https://github.com/sphinx-doc/sphinx/blob/9e1b4a8f1678e26670d34765e74edf3a3be3c62c/sphinx/directives/other.py
"""

from typing import Any, Callable, Dict

import docutils.core
from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives.misc import Class, Include


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


class toctree(nodes.General, nodes.Element):
    ...


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
        container = toctree()
        container['parent'] = self.state.document.current_source
        container['entries'] = []
        container['includefiles'] = []
        container['maxdepth'] = self.options.get('maxdepth', -1)
        container['caption'] = self.options.get('caption')
        container['glob'] = 'glob' in self.options
        container['hidden'] = 'hidden' in self.options
        container['includehidden'] = 'includehidden' in self.options
        container['numbered'] = self.options.get('numbered', 0)
        container['titlesonly'] = 'titlesonly' in self.options

        wrappernode = nodes.compound(classes=['toctree-wrapper'])
        wrappernode.append(container)
        self.add_name(wrappernode)

        ret = self.parse_content(container)
        ret.append(container)
        return ret

    def parse_content(self, container):
        ret = []
        for entry in self.content:
            if not entry:
                continue
            container['entries'].append(nodes.paragraph('', entry))

        return ret


def setup():
    directives.register_directive('toctree', TocTree)
    directives.register_directive('only', Only)
    directives.register_directive('rst-class', Class)
    directives.register_directive('include', Include)
