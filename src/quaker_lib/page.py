import os
import docutils
import docutils.core
from quaker_lib.directives.metadata import get_metadata

from docutils import nodes
from types import SimpleNamespace
from quaker_lib.util import make_id
from quaker_lib.directives.sphinx import ref_role


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

        ref_role.page = self
        self.main.docutil_settings['env'].docname = self.src.name

        # Parse the file contents.
        self.doctree = docutils.core.publish_doctree(
            content,
            parser=self.main.source_parsers.get(self.src.suffix)(),
            source_path=str(self.src),
            settings_overrides={
                **self.main.docutil_settings,
                'page': self,
                'main': self.main,
            }
        )

        # Find the page title.
        try:
            self.title = next(iter(self.doctree.traverse(nodes.title)))[0]
            self.title = self.title.astext()
        except StopIteration:
            self.title = ''

        self.handle_references(self.main)

        # Write if all the references are already resolved.
        if self.unresolved_references == 0:
            self.write()

    def use_reference(self, ref):
        """TODO"""
        if (ref.count('.') >= 2
                or ref.startswith('https://')
                or ref.startswith('http://')):
            return ref

        ref = make_id(ref)

        # If absolute path simply add to waiting list.
        if ref[0] == '/':
            pass
        # TODO
        elif ref[0] == '#':
            ref = make_id(str(self.path) + '#' + ref[1:])
        # If relative path prepend the current path.
        elif '/' in ref or '.' in ref or '#' in ref:
            ref = make_id(str(self.path.parent / ref))
        # Otherwise assume (global) id (else user should prepend ./).
        else:
            pass

        if ref not in self.main.id_map:
            self.main.waiting[ref].append(self)
            self.unresolved_references += 1

        return ref

    def id_to_map(self, id, node, anchor=''):
        """ TODO """
        references = [id, str(self.path.with_suffix('')) + anchor]

        contents = SimpleNamespace()
        contents.url = self.path_html + anchor
        contents.title = None
        contents.sections = []  # We will fill these later.

        # Get the title.
        title_node = node.next_node(nodes.Titular)
        if title_node:
            contents.title = title_node.astext()

        # Add all references.
        for ref in references:
            self.main.id_map[ref] = contents

        return references

    def handle_references(self, main):
        """TODO"""

        page_id = make_id(str(self.path.name))

        # Add all the ids to the reference map.
        all_references = self.id_to_map(page_id, self.doctree)

        for id, node in self.doctree.ids.items():
            all_references += self.id_to_map(id, node, anchor='#' + id)

        # Loop over the sections of this node, and add these to the
        # contents of this page's reference.
        stack = [self.doctree]
        first = True
        while stack:
            node = stack.pop()
            if not node.attributes['ids']:
                continue

            id = node.attributes['ids'][0]
            sections = self.main.id_map[id].sections

            if first:
                first = False
                self.main.id_map[all_references[1]].sections = sections

            for id in node.attributes['ids'][1:]:
                self.main.id_map[id].sections = sections

            # Fill the sections:
            for child in node.children:
                if not isinstance(child, nodes.section):
                    continue

                id = child.attributes['ids'][0]
                id = make_id(str(self.path) + '#' + id)
                sections.append(id)

                # Go over the subsections.
                if len(child.children) > 0:
                    stack.append(child)

        # Resolve all the references we have added.
        for ref in all_references:
            try:
                for page in self.main.waiting.pop(ref):
                    page.unresolved_references -= 1
                    if page.unresolved_references == 0:
                        page.write()
            except KeyError:
                pass

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
            'html_path': self.path_html,
            'embed_stylesheet': False,
            'rel_base': os.path.relpath(self.main.dest_path,
                                        self.dest.parent),
            'handlers': self.main.sp_app.get_handlers(),
            'favicon': self.main.conf_vars.get('html_favicon', None),
            'logo': self.main.conf_vars.get('html_logo', None),
            'copyright': self.main.conf_vars.get('copyright', ''),
            'id_map': self.main.id_map
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
        metadata = get_metadata(self.doctree)
        if metadata.ignore:
            return

        # Delete the nodes we want to skip.
        self.del_skipped_nodes()

        # Collect all the text content to add the page to the index.
        content = ' '.join(n.astext()
                           for n in self.doctree.traverse(nodes.Text))
        self.main.idx.add_file(content, self.title,
                               self.path_html, metadata.priority)

        # Create the output file contents.
        output = docutils.core.publish_from_doctree(
            self.doctree,
            destination_path=self.dest,
            writer=self.main.writer(),
            settings_overrides=self.get_settings_overrides())

        # Write the document to a file.
        self.dest.parent.mkdir(parents=True, exist_ok=True)
        self.dest.write_bytes(output)
