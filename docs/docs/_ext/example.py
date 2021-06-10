import html

from docutils import nodes
from sphinx.locale import _
from docutils.nodes import Element, Admonition
from sphinx.util.docutils import SphinxDirective
from docutils.parsers.rst.roles import set_classes
from docutils.parsers.rst.directives.admonitions import BaseAdmonition

EXAMPLE_NUMBER = 0
EXAMPLE_MAPPING = set()


class example(nodes.Admonition, nodes.Element):
    def __init__(self, text, title, **kwargs):
        super().__init__(text, **kwargs)
        global EXAMPLE_NUMBER
        EXAMPLE_NUMBER += 1

        if title:
            self.title_text = html.escape(f'Example: {title}')
        else:
            self.title_text = 'Example'

        if title:
            link_id = title.replace(' ', '-')
        else:
            link_id = '-'.join(text.split(' ')[:5])

        link_id = 'Example-' + html.escape(link_id).lower()
        if link_id in EXAMPLE_MAPPING:
            link_id += f'-{EXAMPLE_NUMBER}'
        else:
            EXAMPLE_MAPPING.add(link_id)

        self.link_id = link_id


class ExampleDirective(BaseAdmonition):
    node_class = example
    optional_arguments = 1

    def run(self):
        set_classes(self.options)
        self.assert_has_content()
        text = '\n'.join(self.content)
        if self.arguments:
            title_text = self.arguments[0]
        else:
            title_text = ''
        admonition_node = self.node_class(text, title_text, **self.options)
        self.add_name(admonition_node)

        self.state.nested_parse(
            self.content, self.content_offset, admonition_node
        )
        return [admonition_node]


def visit_example_node(self, node):
    self.body.append(
        self.starttag(node, 'div', CLASS=('admonition example-directive'))
    )

    node.insert(
        0,
        nodes.raw(
            '',
            (
                f'<p class="first admonition-title" id="{node.link_id}">' + (
                    f'{node.title_text}' + (
                        f'<a class="headerlink" href="#{node.link_id}"'
                        f' title="Permalink to this'
                        f' example">{self.permalink_text}</a>'
                    )
                ) + '<p>'
            ),
            format='html',
        )
    )

    self.set_class_on_child(node, 'first', 0)
    self.set_class_on_child(node, 'last', -1)


def depart_example_node(self, node):
    self.depart_admonition(node)


def setup(app):
    app.add_node(
        example,
        html=(visit_example_node, depart_example_node),
        latex=(visit_example_node, depart_example_node),
        text=(visit_example_node, depart_example_node)
    )
    app.add_directive('example', ExampleDirective)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
