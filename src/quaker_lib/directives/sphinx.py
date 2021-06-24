"""
Implement directives used by Sphinx

All implementations of the directives have been inspired by:
`https://github.com/sphinx-doc/sphinx/blob/4.x/sphinx/directives/other.py`
"""

from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives, roles
from docutils.parsers.rst.roles import set_classes
from docutils.parsers.rst.directives.misc import Class, Include
from importlib import import_module
import inspect

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

from quaker_lib import util


class kbd_element(nodes.General, nodes.Element):
    """
    Empty node for rendering keyboard inputs
    """
    pass


class toc_data(nodes.General, nodes.Element):
    """Node representing the ToC data.

    Stores the configuration options of the given ToC as well as the references
    given. It is also responsible for it's own html translation.

    """
    def create_html(self, id_map: dict, css_class: str = 'toc'):
        """Turn the contents of the ToC into a html table.

        Parameters
        ----------
        id_map : dict
            Dictionary mapping the references to content objects.
        css_class : str
            Specify which css class the toc uses.

        Returns
        -------
        body : list
            List of html strings.

        """
        # Make max_depth and collapse depth complete if -1.
        max_depth = self['maxdepth']
        if max_depth < 0:
            max_depth = 10000

        collapse_depth = self['collapsedepth']
        if collapse_depth < 0:
            collapse_depth = max_depth

        list_tag = 'ol' if self['numbered'] else 'ul'

        body = [f'<p class="caption {css_class}-label">\n'
                '\t<span class="caption-text">\n'
                f'\t{self["caption"]}\n\t\t</span>\n\t</p>'
                f'<{list_tag}{self.get_numbered_type(0)} '
                f'class="{css_class}-list">\n']

        stack = [list(reversed(self['entries']))]
        while stack:
            depth = len(stack)
            if not stack[-1]:
                stack.pop()
                continue

            current = stack[-1].pop()
            tab_size = depth * '\t'

            if current is None:
                # Print end of the sublist.
                body.append(tab_size)
                body.append(f'</{list_tag}>\n')
                body.append('</li>\n')
                continue

            collapsed = ' is-collapsed' if depth > collapse_depth else ''

            title, ref_id = current
            body.append('<li><span class="level mb-0"><a ')

            ref = id_map.get(ref_id, None)
            if ref is not None:
                if title is None:
                    title = ref.url if ref.title is None else ref.title

                if '#' in ref.url:
                    body.append(f'onClick="expandSidebar(\'{ref.url}\')" ')

                body.append(f'href="{ref.url}">{title}</a>')

                if len(ref.sections) > 0 and depth < max_depth:
                    if collapsed:
                        body.append('<span onclick='
                                    '"toggleExpand(this.parentNode)"'
                                    ' class="is-clickable icon is-small '
                                    'level-right">'
                                    '<i class="fa arrow-icon fa-angle-right" '
                                    'aria-hidden="true"></i></span>')

                    body.append('</span>')
                    body.append(f'<{list_tag}{self.get_numbered_type(depth)} '
                                f'class="{css_class}-list{collapsed}">\n')

                    new = [None] + [(None, sec)
                                    for sec in reversed(ref.sections)]
                    stack.append(new)
                else:
                    body.append('</span></li>\n')
            else:
                if title is None:
                    title = ref_id
                body.append(f'href="{ref_id}">{title}</a></span></li>\n')

        body.append(f'</{list_tag}>\n')
        return body

    def get_numbered_type(self, depth: int):
        """ Helper method to get the type of number labels for enumerates. """
        if self['numbered']:
            nt = self['number_types']
            return f' type="{nt[depth % len(nt)]}"'
        else:
            return ''


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
    """Directive for generating a Table of Contents

    This also includes the generation of the navbar as this uses the ToC
    outlined in the master file of the website.

    Attributes
    ----------
    has_content : bool
        Tell docutils that this directive uses it's content.
    option_spec : dict
        Tell docutils which options are needed and their types.

    """
    has_content = True

    option_spec = {
        'maxdepth': int,
        'collapsedepth': int,
        'name': directives.unchanged,
        'caption': directives.unchanged_required,
        'numbered': directives.flag,
        'number_types': directives.unchanged,
        'hidden': directives.flag,
        # Ignore:
        'glob': directives.flag,
        'includehidden': directives.flag,
        'titlesonly': directives.flag,
        'reversed': directives.flag,
    }

    def run(self):
        """Code that is being run for the directive.

        Returns
        -------
        [tocdata] : list
            A node containing the information necessary for the ToC.

        """
        tocdata = toc_data()
        tocdata['maxdepth'] = self.options.get('maxdepth', -1)
        tocdata['collapsedepth'] = self.options.get('collapsedepth', 1)
        tocdata['caption'] = self.options.get('caption', '')
        tocdata['reversed'] = 'reversed' in self.options
        tocdata['numbered'] = 'numbered' in self.options
        tocdata['number_types'] = self.options.get('number_types', '1 a i A I')
        tocdata['number_types'] = tocdata['number_types'].split()
        tocdata['hidden'] = 'hidden' in self.options

        tocdata['entries'] = self.parse_content()
        return [tocdata]

    def parse_content(self):
        """ Fill the toctree data structure with entries. """
        result = []
        # Add each entry to the list as a title and reference tuple.
        for entry in self.content:
            # Check if current entry is in format 'Some Title <some_link>'.
            explicit_link = util.link_explicit(entry)

            if explicit_link:
                title, ref = explicit_link
            else:
                title = None
                ref = entry

            # Get the actual reference from the id_map using the appropriate
            # logic safely.
            ref = self.state.document.settings.page.use_reference(ref)
            result.append((title, ref))
        return result


class CodeBlock(Directive):
    """Directive for displaying code samples.

    Attributes
    ----------
    has_content : bool
        Tell docutils that this directive uses it's content.
    option_spec : dict
        Tell docutils which options are needed and their types.
    optional_arguments : int
        Tell docutils how many optional arguments to expect.
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
        """ Create nodes for this directive. """
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


class AutoModule(Directive):
    """
    Directive for automatically documenting a Python module.
    """
    required_arguments = 1
    option_spec = {
        'members': directives.flag,
        'show-inheritance': directives.flag,
        'undoc-members': directives.flag
    }

    class_translation = {
        'type': 'class',
        'function': 'def'
    }

    def run(self):
        """
        Create nodes for this directive.
        """
        modname = self.arguments[0]
        mod = import_module(modname)

        ret = nodes.compound(classes=['automodule'])
        ret.append(nodes.emphasis('', modname))
        ret.append(nodes.term('', mod.__doc__))
        if 'members' in self.options:
            members = [(i, getattr(mod, i)) for i in dir(mod)
                       if not i.startswith('__')
                       and not inspect.ismodule(getattr(mod, i))]
            members = [(m, n) for m, n in members
                       if hasattr(n, '__module__') and n.__module__ == modname]

            for member in members:
                node = nodes.definition_list()
                mem_type = type(member[1]).__name__

                if mem_type == 'type':
                    init_params = inspect.getargspec(member[1].__init__).args
                    function_params = f'({", ".join(init_params)})'
                elif mem_type == 'function':
                    params = inspect.getargspec(member[1]).args
                    function_params = f'({", ".join(params)})'

                type_name = self.class_translation.get(mem_type, mem_type)
                items = [
                    nodes.emphasis('', f'{type_name}', classes=['type_name']),
                    nodes.emphasis('', f'{modname}.'),
                    nodes.emphasis('', member[0]),
                    nodes.emphasis('', function_params),
                    nodes.term('', member[1].__doc__)
                ]

                # TODO: Display member attributes/methods?

                node.append(nodes.definition_list_item('', *items))
                ret.append(node)

        return [ret]


def ref_role(role, rawtext, text, lineno, inliner, options={}, content=[]):
    """
    Role for creating hyperlink to other documents.
    """
    explicit_link = util.link_explicit(text)

    if explicit_link is not None:
        title, ref = explicit_link
    else:
        ref, title = text, None

    node = ref_element()
    node['title'] = title
    node['ref'] = ref_role.page.use_reference(ref)

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
    directives.register_directive('include', Include)
    directives.register_directive('toctree', TocTree)
    directives.register_directive('code-block', CodeBlock)
    directives.register_directive('automodule', AutoModule)

    roles.register_canonical_role('ref', ref_role)
    roles.register_canonical_role('kbd', kbd_role)
