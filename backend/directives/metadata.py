from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives

class MetaData(Directive):
    has_content = True

    def run(self):
        print(self.content)


def setup():
    directives.register_directive('metadata', MetaData)
