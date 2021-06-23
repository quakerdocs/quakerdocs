import os
import docutils
import directives.metadata
from docutils import nodes
from types import SimpleNamespace
from directives.sphinx import ref_element
from util import make_id


class Page:
    """Handler for a single page.

    Parameters
    ----------
    main : Main
        The instance of main, from which settings are extracted.
    path : pathlib.Path
        The path to the file to be handled.

    Attributes
    ----------
    id_map : dict
        An index shared by all Page instances, to track references.
    """
    id_map = {}

    def __init__(self, main, path):
        self.main = main
        self.path = path
        self.path_html = str(path.with_suffix('.html'))
        self.src = main.source_path / path
        self.dest = main.dest_path / self.path_html
        self.doctree = None
        self.unresolved_references = 0

    def parse(self):
        """
        Parse an RST file.
        """
        # Add prologue and epilogue to source file.
        content = (f"{self.main.conf_vars.get('rst_prolog', '')}\n"
                   f"{self.src.read_text()}\n"
                   f"{self.main.conf_vars.get('rst_epilog', '')}")

        # Parse the file contents.
        self.doctree = docutils.core.publish_doctree(
            content,
            source_path=str(self.src),
            settings_overrides={
                **self.main.docutil_settings,
                'page': self,
                'main': self.main,
                'path': self.path #TODO remove
            }
        )

        self.handle_references(self.main)

        # Check if the file can be written,
        # for node in self.doctree.traverse(ref_element):
        #     self.use_reference(node['ref'])

        # Write if all the references are already resolved.
        if self.unresolved_references == 0:
            self.write(self.main)

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
            contents.sections = []  # We will fill these later.

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
            contents = main.id_map[id]

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

    def get_settings_overrides(self):
        """Get the settings_override for this page.
        Used as arg for the call to docutils.core.publish_from_doctree
        in write.

        Returns
        -------
        dict
            The argument expected by publish_from_doctree.
        """
        return {
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
            'id_map': self.id_map
        }

    def del_skipped_nodes(self):
        """Delete the nodes from the page's doctree that match SKIP_TAGS."""
        for node in self.doctree.traverse():
            for i, child in reversed(list(enumerate(node.children))):
                if child.tagname in self.main.SKIP_TAGS:
                    del node[i]

    def write(self):
        """
        Parse an RST file and write its contents to a file.
        """

        # Get the page metadata.
        metadata = directives.metadata.get_metadata(self.doctree)
        if metadata.ignore:
            return

        # Delete the nodes we want to skip.
        self.del_skipped_nodes()

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
            settings_overrides=self.get_settings_overrides())

        # Write the document to a file.
        self.dest.parent.mkdir(parents=True, exist_ok=True)
        self.dest.write_bytes(output)
