"""
Class to extend the functionality of the default HTML5 writer of docutils.
"""

import os.path
from docutils import nodes
import docutils.writers.html5_polyglot


class Writer(docutils.writers._html_base.Writer):
    """
    Writer class for HTML5 documents.
    This class is modified from docutils html5_polyglot.Writer (Jun 2021)
    """
    default_stylesheets = []
    default_stylesheet_dirs = ['.', os.path.abspath(os.path.dirname(__file__))]

    default_template = '../quaker_theme/template.txt'
    default_template_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), default_template)

    settings_spec = (
        'Quaker HTML Options',
        None,
        (
            ('Comma separated list of stylesheet URLs. '
             'Overrides previous --stylesheet and --stylesheet-path settings.',
             ['--stylesheet'],
             {'metavar': '<URL[,URL,...]>', 'overrides': 'stylesheet_path'}),
            ('Comma separated list of stylesheet paths.',
             ['--stylesheet-path'],
             {'metavar': '<file[,file,...]>', 'overrides': 'stylesheet',
              'default': default_stylesheets}),
            ('Embed the stylesheet(s) in the output HTML file.',
             ['--embed-stylesheet'],
             {'default': 1, 'action': 'store_true'}),
            ('Link to the stylesheet(s) in the output HTML file.',
             ['--link-stylesheet'],
             {'dest': 'embed_stylesheet', 'action': 'store_false'}),
            ('List of directories where stylesheets are found.',
             ['--stylesheet-dirs'],
             {'metavar': '<dir[,dir,...]>',
              'default': default_stylesheet_dirs}),
            ('Specify the initial header level.',
             ['--initial-header-level'],
             {'choices': '1 2 3 4 5 6'.split(), 'default': '2',
              'metavar': '<level>'}),
            ('Format for footnote references',
             ['--footnote-references'],
             {'choices': ['superscript', 'brackets'], 'default': 'brackets',
              'metavar': '<format>',
              'overrides': 'trim_footnote_reference_space'}),
            ('Format for block quote attributions',
             ['--attribution'],
             {'choices': ['dash', 'parentheses', 'parens', 'none'],
              'default': 'dash', 'metavar': '<format>'}),
            ('Remove extra vertical whitespace between items of bullet '
             'lists and enumerated lists.',
             ['--compact-lists'],
             {'default': True, 'action': 'store_true'}),
            ('Disable compact simple bullet and enumerated lists.',
             ['--no-compact-lists'],
             {'dest': 'compact_lists', 'action': 'store_false'}),
            ('Remove extra vertical whitespace between items of simple field '
             'lists.',
             ['--compact-field-lists'],
             {'default': True, 'action': 'store_true'}),
            ('Disable compact simple field lists.',
             ['--no-compact-field-lists'],
             {'dest': 'compact_field_lists', 'action': 'store_false'}),
            ('Embed images in the output HTML file, if the image '
             'files are accessible during processing.',
             ['--embed-images'],
             {'default': 0, 'action': 'store_true'}),
            ('Link to images in the output HTML file.',
             ['--link-images'],
             {'dest': 'embed_images', 'action': 'store_false'}),
            ('Added to standard table classes. '
             'Defined styles: borderless, booktabs, '
             'align-left, align-center, align-right, colwidths-auto.',
             ['--table-style'],
             {'default': ''}),
            ('Math output format (one of "MathML", "HTML", "MathJax", '
             'or "LaTeX") and option(s).',
             ['--math-output'],
             {'default': 'HTML ../quaker_theme/static/css/math.css'}),
            ('Prepend an XML declaration.',
             ['--xml-declaration'],
             {'default': False, 'action': 'store_true'}),
            ('Obfuscate email addresses to confuse harvesters.',
             ['--cloak-email-addresses'],
             {'default': False, 'action': 'store_true'}),
        ))

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
        super().__init__()
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
        self.settings = document.settings

        # Set base path for every document.
        self.head.append(f'<base href="{self.settings.rel_base}">')

        # Add favicon to pages.
        if self.settings.favicon is not None:
            self.head.append('<link rel="icon" '
                             f'href="{self.settings.favicon}">')

        # Build navigation bar.
        # self.navigation = ''
        # for toc in self.settings.toc:
        #     self.navigation += directives.sphinx.TocTree.to_html(toc)
        self.navigation = '<div id="navigation-tree"></div>'

        # Add logo to pages.
        self.logo = ''
        if self.settings.logo is not None:
            self.logo = f'<img src="{self.settings.logo}" alt="Logo">'

        link = 'https://quakerdocs.nl/'

        self.footer.append(
            f'<p>&copy {self.settings.copyright}.</p>'
            '<p>Generated with <span style="color: red"> '
            '<i class="fas fa-heart"></span></i> & '
            '<span style="color: #ffcc4d"><i class="fas fa-beer"></i></span> '
            f'<a href="{link}"> QuakerDocs</a></p>')

    def visit_metadata(self, node: nodes.Element):
        """
        Skip rendering of metadata data-element.
        """
        raise nodes.SkipNode

    def visit_toc_data(self, node: nodes.Element):
        """
        Render the Table of Contents data-element.
        """
        if node['hidden']:
            raise nodes.SkipNode
            return

        for i in node.create_html(self.settings.id_map):
            self.body.append(i)

    def depart_toc_data(self, node: nodes.Element):
        pass

    def visit_pending_xref(self, node: nodes.Element):
        """
        ...
        """
        raise nodes.SkipNode

    def visit_ref_element(self, node: nodes.Element):
        """
        Find reference belonging to this element.
        """
        title = node['title']
        if node['ref'] in self.settings.id_map:
            ref = self.settings.id_map[node['ref']]

            # Make sure the title exists.
            if title is None:
                title = ref if ref.title is None else ref.title

            self.body.append(f'<a href="{ref.url}">{title}</a>')
        else:
            if title is not None:
                self.body.append(title)

    def depart_ref_element(self, node: nodes.Element):
        """
        End of rendering reference.
        """

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
        bookmark_id = self.create_bookmark_id(node)
        onclick = f"bookmarkClick('{bookmark_id}')"
        html = (f'<button id="{bookmark_id}" class="bookmark-btn" '
                f'onclick="{onclick}" title="{title}" value=0>'
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
