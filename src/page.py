import os
import docutils
import application
import directives.metadata
from docutils import nodes
from directives.sphinx import ref_element


class Page:
    """Handler for a single page.

    Parameters
    ----------
    main : Main
        The instance of main, from which settings are extracted.
    path : pathlib.Path
        The path to the file to be handled.
    """

    def __init__(self, main, path):
        self.main = main
        self.path = path

        self.html_path = str(path.with_suffix('.html'))
        self.src = main.source_path / path
        self.dest = main.dest_path / self.html_path
        self.doctree = None
        self.unresolved_references = 0

    def parse(self):
        """
        Parse an RST file.
        """

        content = (f"{self.main.conf_vars.get('rst_prolog', '')}\n"
                   f"{self.src.read_text()}\n"
                   f"{self.main.conf_vars.get('rst_epilog', '')}")

        self.doctree = docutils.core.publish_doctree(
            content,
            source_path=str(self.src),
            settings_overrides={
                **self.main.docutil_settings,
                'src_path': self.path
            }
        )

        for page_id in self.doctree.ids:
            application.id_map.update({page_id: self.html_path})

            # Resolve the references of the waiting pages.
            if page_id in self.main.waiting:
                for page in self.main.waiting[page_id]:
                    page.unresolved_references -= 1
                    if page.unresolved_references == 0:
                        page.write(self.main)

                self.main.waiting.pop(page_id)

        # Check if the file can be written,
        for node in self.doctree.traverse(ref_element):
            if node['ref'] not in application.id_map:
                self.main.waiting[node['ref']].append(self)
                self.unresolved_references += 1

        # Write if all the references are already resolved.
        if self.unresolved_references == 0:
            self.write()

    def get_title(self):
        """Get the title of the page.

        Returns
        -------
        title : str
            The title of the page.
        """
        # TODO this is the biggest hack I've ever seen.
        try:
            return next(iter(self.doctree.traverse(nodes.title)))[0].astext()
        except StopIteration:
            return

    def write(self):
        """
        Parse an RST file and write its contents to a file.
        """

        # Get the page metadata.
        metadata = directives.metadata.get_metadata(self.doctree)
        if metadata.ignore:
            return

        # Delete the nodes we want to skip.
        for node in self.doctree.traverse():
            for i, child in reversed(list(enumerate(node.children))):
                if child.tagname in self.main.SKIP_TAGS:
                    del node[i]

        # Find the page title.
        title = self.get_title()

        # Collect all the text content to add the page to the index.
        content = ' '.join(n.astext()
                           for n in self.doctree.traverse(nodes.Text))
        self.main.idx.add_file(content, title,
                               self.html_path, metadata.priority)

        # Create the output file contents.
        output = docutils.core.publish_from_doctree(
            self.doctree,
            destination_path=self.dest,
            writer=self.main.writer(),
            settings_overrides={
                'toc': self.main.toc_navigation,
                'template': self.main.theme.get_template(),
                'stylesheet': os.path.join(
                    '_static',
                    self.main.conf_vars.get('html_style',
                                            self.main.theme.get_style())),
                'src_dir': self.main.source_path,
                'dest_dir': self.main.relative_path(self.src),
                'html_path': self.html_path,
                'embed_stylesheet': False,
                'rel_base': os.path.relpath(self.main.dest_path,
                                            self.dest.parent),
                'handlers': self.main.sp_app.get_handlers(),
                'favicon': self.main.conf_vars.get('html_favicon', None),
                'logo': self.main.conf_vars.get('html_logo', None),
                'copyright': self.main.conf_vars.get('copyright', ''),
                'id_map': application.id_map
            })

        # Write the document to a file.
        self.dest.parent.mkdir(parents=True, exist_ok=True)
        self.dest.write_bytes(output)
