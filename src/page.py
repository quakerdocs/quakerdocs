import os
import docutils
import directives.metadata
from docutils import nodes
from types import SimpleNamespace
from directives.sphinx import ref_element
from util import make_id

class Page():
    """TODO
    """

    def __init__(self, main, path):
        self.path = path
        self.path_html = str(path.with_suffix('.html'))
        self.src = main.source_path / path
        self.dest = main.dest_path / self.path_html
        self.doctree = None
        self.unresolved_references = 0

        self.main = main

    def parse(self, main):
        """
        Parse a rst file.
        """

        content = self.src.read_text()

        # Add epilogue and prolog to source file.
        content = '%s\n%s\n%s' % (
            main.conf_vars.get('rst_prolog', ''),
            content,
            main.conf_vars.get('rst_epilog', ''))

        # Parse the file contents.
        self.doctree = docutils.core.publish_doctree(
            content,
            source_path=str(self.src),
            settings_overrides={
                **main.docutil_settings,
                'page': self,
                'main': main
            }
        )

        self.handle_references(main)

        # Check if the file can be written,
        # for node in self.doctree.traverse(ref_element):
        #     self.use_reference(node['ref'])

        # Write if all the references are already resolved.
        if self.unresolved_references == 0:
            self.write(main)

    def use_reference(self, ref):
        """TODO"""
        if ref not in self.main.id_map:
            self.main.waiting[ref].append(self)
            self.unresolved_references += 1

    def handle_references(self, main):
        """TODO"""
        print(self.path, '\n')

        page_id = make_id(self.path.name)
        all_references = []

        # Add all the ids to the reference map.
        first = True
        for id, node in [(page_id, self.doctree), *self.doctree.ids.items()]:
            anchor = ''
            if not first:
                anchor = '#' + id
            first = False

            references = [id, str(self.path.with_suffix('')) + anchor]
            all_references += references

            contents = SimpleNamespace()
            contents.url = self.path_html + anchor
            contents.title = None
            contents.sections = [] # We will fill these later.

            # Get the title.
            title_node = node.next_node(nodes.Titular)
            if title_node:
                title = title_node.astext()

            # Add all references.
            for ref in references:
                main.id_map[ref] = contents

        # Loop over the sections of this node, and add these to the
        # contents of this page's reference.
        stack = [self.doctree]
        while stack:
            node = stack.pop()
            id = node.attributes['ids'][0]
            contents = main.map_id[id]

            # Fill the sections:
            for child in node.children:
                if not isinstance(child, nodes.section):
                    continue

                id = child.attributes['ids'][0]
                contents.sections.append(id)

                # Only continue if the current section contains a title.
                if len(child.children) > 0:
                    # Use id of the anchor, not of the section!
                    stack.append(child)

        # Resolve all the references we have added.
        for ref in all_references:
            if ref in self.main.waiting:
                for page in self.main.waiting[ref]:
                    page.unresolved_references -= 1
                    if page.unresolved_references == 0:
                        page.write(self.main)

                self.main.waiting.pop(ref)

        exit(0)
        # Loop over the sections to create the content lists


    def write(self, main):
        """
        Parse a rst file and write its contents to a file.
        """

        # Get the page metadata.
        metadata = directives.metadata.get_metadata(self.doctree)
        if metadata.ignore:
            return

        # Delete the nodes we want to skip.
        for node in self.doctree.traverse():
            for i, child in reversed(list(enumerate(node.children))):
                if child.tagname in main.SKIP_TAGS:
                    del node[i]

        # Find the page title.
        try:
            title = next(iter(self.doctree.traverse(nodes.title)))[0].astext()
        except StopIteration:
            title = ''

        # Collect all the text content to add the page to the index.
        content = ' '.join(n.astext() for n in self.doctree.traverse(
                           lambda n: isinstance(n, nodes.Text)))
        main.idx.add_file(content, title, self.path_html, metadata.priority)

        # Create the output file contents.
        output = docutils.core.publish_from_doctree(
            self.doctree,
            destination_path=self.dest,
            writer=main.writer(),
            settings_overrides={
                'toc': main.toc_navigation,
                'template': main.theme.get_template(),
                'stylesheet': os.path.join(
                    '_static', main.conf_vars.get('html_style',
                                                  main.theme.get_style())),
                'src_dir': main.source_path,
                'dest_dir': main.relative_path(self.src),
                'html_path': self.path_html,
                'embed_stylesheet': False,
                'rel_base': os.path.relpath(main.dest_path, self.dest.parent),
                'handlers': main.sp_app.get_handlers(),
                'favicon': main.conf_vars.get('html_favicon', None),
                'logo': main.conf_vars.get('html_logo', None),
                'copyright': main.conf_vars.get('copyright', ''),
                'id_map': main.id_map
            })

        # Write the document to a file.
        self.dest.parent.mkdir(parents=True, exist_ok=True)
        self.dest.write_bytes(output)
