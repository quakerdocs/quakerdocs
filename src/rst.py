import os
import docutils
import application
import directives.metadata
from docutils import nodes

class Rst():

    def __init__(self, main, path):
        self.html_path = str(path.with_suffix('.html'))
        self.src = main.source_path / path
        self.dest = main.dest_path / self.html_path
        self.doctree = None

    def parse(self, main):
        """
        Parse a rst file.
        """

        with self.src.open() as f:
            content = f.read()

        # Add epilogue and prolog to source file.
        content = '%s\n%s\n%s' % (
            main.conf_vars.get('rst_prolog', ''),
            content,
            main.conf_vars.get('rst_epilog', ''))

        self.doctree = docutils.core.publish_doctree(
            content,
            source_path=str(self.src),
            settings_overrides=main.docutil_settings
        )

        for page_id in self.doctree.ids:
            application.id_map.update({page_id: self.html_path})

            if page_id in main.waiting:
                rst = main.waiting[page_id]


        for node in self.doctree.traverse(lambda n: isinstance(n, ref_element)):
            if node['ref'] not in application.id_map:
                main.waiting[node['ref']] = self

        return True

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
        main.idx.add_file(content, title, self.html_path, metadata.priority)

        # Create the output file contents.
        output = docutils.core.publish_from_doctree(
            self.doctree,
            destination_path=self.dest,
            writer=main.Builder(),
            settings_overrides={
                'toc': main.toc_navigation,
                'src_dir': main.source_path,
                'html_path': self.html_path,
                'rel_base': os.path.relpath(main.dest_path, self.dest.parent),
                'handlers': main.sp_app.get_handlers(),
                'favicon': main.conf_vars.get('html_favicon', None),
                'logo': main.conf_vars.get('html_logo', None),
                'copyright': main.conf_vars.get('copyright', ''),
                'html_style': main.conf_vars.get('html_style', None),
                'id_map': application.id_map
            })

        # Write the document to a file.
        with open(self.dest, 'wb') as f:
            f.write(output)
