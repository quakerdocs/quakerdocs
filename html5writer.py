"""
Class to extend the functionality of the default HTML5 writer of docutils.
"""

from docutils import nodes
import docutils.writers.html5_polyglot


# Modified from docutils html5_polyglot implementation
class Writer(docutils.writers.html5_polyglot.Writer):
    def __init__(self):
        docutils.writers.html5_polyglot.Writer.__init__(self)
        self.translator_class = HTMLTranslator


class HTMLTranslator(docutils.writers.html5_polyglot.HTMLTranslator):
    def visit_toctree(self, node: nodes.Element):
        self.body.append('<p>Hey</p>')

    def depart_toctree(self, node: nodes.Element):
        self.body.append('<p>Hey</p>')
