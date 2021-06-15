"""
Class to extend the functionality of the default HTML5 writer of docutils.
"""

import os.path
from docutils import nodes
import docutils.writers.html5_polyglot

import directives.sphinx


class Writer(docutils.writers._html_base.Writer):
    """
    Writer class for HTML5 documents.
    This class is modified from docutils.writers.html5_polyglot.Writer
    """
    supported = ('html', 'html5')
    """Formats this writer supports."""

    default_stylesheets = []
    default_stylesheet_dirs = ['.', os.path.abspath(os.path.dirname(__file__))]

    default_template = '../static/template.txt'
    default_template_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), default_template)

    settings_spec = (
        'HTML-Specific Options',
        None,
        (('Specify the template file (UTF-8 encoded).  Default is "%s".'
          % default_template_path,
          ['--template'],
          {'default': default_template_path, 'metavar': '<file>'}),
         ('Comma separated list of stylesheet URLs. '
          'Overrides previous --stylesheet and --stylesheet-path settings.',
          ['--stylesheet'],
          {'metavar': '<URL[,URL,...]>', 'overrides': 'stylesheet_path'}),
         ('Comma separated list of stylesheet paths. '
          'Relative paths are expanded if a matching file is found in '
          'the --stylesheet-dirs. With --link-stylesheet, '
          'the path is rewritten relative to the output HTML file. '
          'Default: "%s"' % ','.join(default_stylesheets),
          ['--stylesheet-path'],
          {'metavar': '<file[,file,...]>', 'overrides': 'stylesheet',
           'default': default_stylesheets}),
         ('Embed the stylesheet(s) in the output HTML file.  The stylesheet '
          'files must be accessible during processing. This is the default.',
          ['--embed-stylesheet'],
          {'default': 1, 'action': 'store_true'}),
         ('Link to the stylesheet(s) in the output HTML file. '
          'Default: embed stylesheets.',
          ['--link-stylesheet'],
          {'dest': 'embed_stylesheet', 'action': 'store_false'}),
         ('Comma-separated list of directories where stylesheets are found. '
          'Used by --stylesheet-path when expanding relative path arguments. '
          'Default: "%s"' % default_stylesheet_dirs,
          ['--stylesheet-dirs'],
          {'metavar': '<dir[,dir,...]>',
           'default': default_stylesheet_dirs}),
         ('Specify the initial header level.  Default is 2 for "<h2>".  '
          'Does not affect document title & subtitle (see --no-doc-title).',
          ['--initial-header-level'],
          {'choices': '1 2 3 4 5 6'.split(), 'default': '2',
           'metavar': '<level>'}),
         ('Format for footnote references: one of "superscript" or '
          '"brackets".  Default is "brackets".',
          ['--footnote-references'],
          {'choices': ['superscript', 'brackets'], 'default': 'brackets',
           'metavar': '<format>',
           'overrides': 'trim_footnote_reference_space'}),
         ('Format for block quote attributions: one of "dash" (em-dash '
          'prefix), "parentheses"/"parens", or "none".  Default is "dash".',
          ['--attribution'],
          {'choices': ['dash', 'parentheses', 'parens', 'none'],
           'default': 'dash', 'metavar': '<format>'}),
         ('Remove extra vertical whitespace between items of "simple" bullet '
          'lists and enumerated lists.  Default: enabled.',
          ['--compact-lists'],
          {'default': True, 'action': 'store_true'}),
         ('Disable compact simple bullet and enumerated lists.',
          ['--no-compact-lists'],
          {'dest': 'compact_lists', 'action': 'store_false'}),
         ('Remove extra vertical whitespace between items of simple field '
          'lists.  Default: enabled.',
          ['--compact-field-lists'],
          {'default': True, 'action': 'store_true'}),
         ('Disable compact simple field lists.',
          ['--no-compact-field-lists'],
          {'dest': 'compact_field_lists', 'action': 'store_false'}),
         ('Embed images in the output HTML file, if the image '
          'files are accessible during processing.',
          ['--embed-images'],
          {'default': 0, 'action': 'store_true'}),
         ('Link to images in the output HTML file. '
          'This is the default.',
          ['--link-images'],
          {'dest': 'embed_images', 'action': 'store_false'}),
         ('Added to standard table classes. '
          'Defined styles: borderless, booktabs, '
          'align-left, align-center, align-right, colwidths-auto. '
          'Default: ""',
          ['--table-style'],
          {'default': ''}),
         ('Math output format (one of "MathML", "HTML", "MathJax", '
          'or "LaTeX") and option(s). '
          'Default: "HTML ../static/css/math.css"',
          ['--math-output'],
          {'default': 'HTML ../static/css/math.css'}),
         ('Prepend an XML declaration. (Thwarts HTML5 conformance.) '
          'Default: False',
          ['--xml-declaration'],
          {'default': False, 'action': 'store_true'}),
         ('Omit the XML declaration.',
          ['--no-xml-declaration'],
          {'dest': 'xml_declaration', 'action': 'store_false'}),
         ('Obfuscate email addresses to confuse harvesters while still '
          'keeping email links usable with standards-compliant browsers.',
          ['--cloak-email-addresses'],
          {'action': 'store_true'}),))

    config_section = 'html5 writer'

    visitor_attributes = (
        'head_prefix', 'head', 'stylesheet', 'body_prefix',
        'body_pre_docinfo', 'docinfo', 'body', 'body_suffix',
        'title', 'subtitle', 'header', 'footer', 'meta', 'fragment',
        'html_prolog', 'html_head', 'html_title', 'html_subtitle',
        'html_body', 'navigation', 'logo')

    def __init__(self):
        """
        Initialize Writer class.
        """
        self.parts = {}
        self.translator_class = HTMLTranslator


class HTMLTranslator(docutils.writers.html5_polyglot.HTMLTranslator):
    """
    Class used for translating internal docutils-nodes to HTML.
    """
    def __init__(self, document):
        """
        Initialize the HTML translator
        """
        super().__init__(document)

        # Set base path for every document.
        self.head.append('<base href="%s">'
                         % document.settings.rel_base)

        # Add favicon to pages.
        if document.settings.favicon is not None:
            self.head.append('<link rel="icon" href="%s">'
                             % document.settings.favicon)

        # Build navigation bar.
        self.navigation = ''
        for toc in document.settings.toc:
            self.navigation += directives.sphinx.TocTree.to_html(toc)

        # Add logo to pages.
        self.logo = ''
        if document.settings.logo is not None:
            self.logo = ('<img src="%s" width="200px" alt="Logo">'
                         % document.settings.logo)

        link = ('https://gitlab-fnwi.uva.nl/'
                'lreddering/pse-documentation-generator')

        self.footer.append(
            f'<p>&copy {document.settings.copyright}.</p>'
            '<p>Generated with &hearts; by '
            f'<a href="{link}">QuakerDocs</a></p>')

    def visit_metadata(self, node: nodes.Element):
        """
        Skip rendering of metadata data-element.
        """
        raise nodes.SkipNode

    def depart_metadata(self, node: nodes.Element):
        """
        Skip rendering of metadata data-element.
        """
        raise nodes.SkipNode

    def visit_toc_data(self, node: nodes.Element):
        """
        Skip rendering of Table of Contents data-element.
        """
        raise nodes.SkipNode

    def depart_toc_data(self, node: nodes.Element):
        """
        Skip rendering of Table of Contents data-element.
        """
        raise nodes.SkipNode

    def visit_kbd_element(self, node: nodes.Element):
        """
        Begin rendering of keystroke element.
        """
        self.body.append('<kbd>')
        self.body.append('+'.join(f'<kbd>{key}</kbd>' for key in node['keys']))

    def depart_kbd_element(self, node: nodes.Element):
        """
        End of rendering keystroke element.
        """
        self.body.append('</kbd>')

    def visit_iframe_node(self, node: nodes.Element) -> None:
        """
        Do nothing on visit.
        """
        pass

    def depart_iframe_node(self, node: nodes.Element) -> None:
        """
        Add iframe HTML with correct attributes.
        """
        url = node['url']
        width = node['width']
        height = node['height']

        code = (f'<iframe src="{url}" width="{width}" height="{height}" '
                'frameborder="0" allow="autoplay"></iframe>')
        self.body.append(code)

    def visit_section(self, node: nodes.Element) -> None:
        """
        Adds a span before the section with the same id as the section.
        """
        if node['ids']:
            section_id = node['ids'][0]
            self.body.append(f'<span class="anchor" id="{section_id}"></span>')
        super().visit_section(node)

    def depart_title(self, node: nodes.Element) -> None:
        """
        Append bookmark button to title element.
        """
        if len(self.context) > 0:
            close_tag = self.context[-1]

            if close_tag.startswith('</h'):
                self.add_bookmark_btn(node)
            super().depart_title(node)

    def add_bookmark_btn(self, node: nodes.Element):
        """
        Add bookmark button for node to the document body.
        """
        title = node.astext()
        id = self.create_bookmark_id(node)
        onclick = f"bookmarkClick('{id}')"
        html = (f'<button id="{id}" class="bookmark-btn" onclick="{onclick}" '
                f'title="{title}" value=0>'
                '<span class="icon"><i class="fa fa-bookmark-o">'
                '</i></span></button>')
        self.body.append(html)

    def create_bookmark_id(self, node: nodes.Element):
        """
        Assign a unique identifier to the bookmark.
        """
        try:
            id_str = "BM_" + str(node.parent['ids'][0])
            return id_str
        except (KeyError, IndexError):
            print('Cannot make bookmark ID, because parent ID can '
                  'not be established.')
            raise
