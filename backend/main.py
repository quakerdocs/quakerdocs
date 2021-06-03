"""
Main entrypoint of the program.
Call this script to invoke the generation of a static document/website.
"""

import os
import argparse
import index
from distutils.dir_util import copy_tree
from docutils import core, io, nodes, readers
import docutils.core
import docutils.writers.html5_polyglot
from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives.misc import Class
from docutils.parsers.rst.directives.misc import Include
import docutils.writers


# https://stackoverflow.com/questions/38834378/path-to-a-directory-as-argparse-argument
def dir_path(string):
    if os.path.isdir(string):
        return string.strip('/')
    else:
        raise NotADirectoryError(string)

SKIP_TAGS = {'system_message', 'problematic'}

class Main:

    def __init__(self, source_path, dest_path, static_path, builder):
        self.source_path = source_path
        self.dest_path = dest_path.strip('/')
        self.static_path = static_path
        self.builder = builder

    def relative_path(self, path):
        """Get the path of a source directory relative to the source file."""
        return path[len(self.source_path)+1:]

    def generate(self):
        """Read all the input files from the source directory, parse them,
        and output the results to the build directory."""
        directives.register_directive('rst-class', Class)
        directives.register_directive('include', Include)

        if not os.path.exists(self.dest_path):
            os.mkdir(self.dest_path)

        self.idx = index.IndexGenerator()

        for root, dirs, files in os.walk(self.source_path):
            for dir in dirs:
                new_dir = os.path.join(self.dest_path, self.relative_path(root), dir)
                if not os.path.exists(new_dir):
                    os.mkdir(new_dir)
            for file in files:
                path = os.path.join(self.relative_path(root), file)
                print("==================== %s ====================" % file)
                try:
                    if file.endswith('.rst'):
                        self.handle_rst(path)
                except FileNotFoundError as e:
                    print(f'File [{file}] not found:', e)
                except docutils.utils.SystemMessage as e:
                    print('DOCUTILS ERROR!', e)

        self.write_index()
        self.copy_static_files()

    def handle_rst(self, path):
        """Parse a rst file and output its contents."""
        src = os.path.join(self.source_path, path)
        dest = os.path.join(self.dest_path, path[:-4] + '.html')

        # Read the rst file.
        doctree = docutils.core.publish_doctree(open(src, 'r').read())

        # Delete the nodes we want to skip.
        for node in doctree.traverse():
            for i, child in reversed(list(enumerate(node.children))):
                if child.tagname in SKIP_TAGS:
                    del node[i]

        # Find the page title.
        try:
            title = next(iter(doctree.traverse(nodes.title)))
            title = title[0].astext()
        except StopIteration:
            title = ''

        # Collect all the text
        content = ' '.join(n.astext() for n in doctree.traverse(lambda n: isinstance(n, nodes.Text)))
        self.idx.parse_file(content, title, path)

        # Export the doctree.
        with open(dest, 'wb') as f:
            f.write(docutils.core.publish_from_doctree(doctree, destination_path=dest,
                                                       writer_name=self.builder))

    def write_index(self):
        """Write the search index file to the destination directory."""
        # Make sure the search directory exist.
        path = os.path.join(self.dest_path, 'search/')
        if not os.path.exists(path):
            os.mkdir(path)

        # Write the search index file.
        with open(os.path.join(path, 'search_index_data.js'), 'w') as f:
            idx_urltitles, idx_index = self.idx.to_json()
            f.write(f'var search_urltitles = ')
            f.write(idx_urltitles)
            f.write(f';\n\nvar search_index = ')
            f.write(idx_index)
            f.write(';\n')

    def copy_static_files(self):
        """Copy all the files from the static path to the destination path."""
        copy_tree(self.static_path, self.dest_path, update=1)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description='SDG')
    arg_parser.add_argument('source_path', type=dir_path, help='The directory containing the RST files.')
    arg_parser.add_argument('-d', type=str, dest='destination_path', default='build', help='The directory to write the output.')
    arg_parser.add_argument('-s', type=dir_path, dest='static_path', default='static', help='The directory to direclty copy from.')
    arg_parser.add_argument('-b', type=str, dest='builder', default="html", help='Builder used for the generator.')
    args = arg_parser.parse_args()

    main = Main(args.source_path, args.destination_path, args.static_path, args.builder)
    main.generate()
