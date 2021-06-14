from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives


class Raw(Directive):
    has_content = True

    def run(self):
        code = "".join(self.content)
        return [nodes.raw('', code, format="html")]


def setup():
    directives.register_directive('raw', Raw)