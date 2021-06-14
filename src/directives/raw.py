from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives

class Raw(Directive):
    has_content = True

    def run(self):
        code = "".join(self.content)
        return []

def setup():
    directives.register_directive('raw', Raw)