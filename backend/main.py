"""
Main entrypoint of the program.
Call this script to invoke the generation of a static document/website.
"""

from sys import stderr
import os
import fnmatch
import argparse

from distutils.dir_util import copy_tree
from docutils import nodes
import docutils.core
import docutils.writers.html5_polyglot
import docutils.parsers.rst
import docutils.writers

import application
import index
import html5writer
import custom_dirs
import spdirs

SKIP_TAGS = {'system_message', 'problematic'}


# https://stackoverflow.com/questions/38834378/path-to-a-directory-as-argparse-argument
def dir_path(string):
    if os.path.isdir(string):
        return string.strip('/')
    else:
        raise NotADirectoryError(string)


class Main:
    # Mapping builder name to (file extension, writer class)
    supported_builders = {
        'html': ('html', html5writer.Writer)
    }

    def __init__(self, source_path, dest_path, builder):
        self.source_path = source_path
        self.dest_path = dest_path
        self.builder = builder

    def relative_path(self, path):
        """
        Get the path of a source directory relative to the source file.
        """
        return path[len(self.source_path)+1:]

    def read_conf(self):
        """
        Read conf.py from the source directory and save the configuration.
        """
        global_vars = {
            '__file__': 'conf.py',
            '__name__': '__main__'
        }
        conf_vars = {}

        # Check if file exists? Other cwd?
        exec(open('conf.py').read(), global_vars, conf_vars)
        self.conf_vars = conf_vars

        # Fix some things
        if 'source_suffix' in self.conf_vars:
            suffix = self.conf_vars['source_suffix']
            if isinstance(suffix, str):
                self.conf_vars['source_suffix'] = [suffix]
        else:
            self.conf_vars['source_suffix'] = ['.rst']

        if 'exclude_patterns' not in self.conf_vars:
            self.conf_vars['exclude_patterns'] = []
        if 'html_static_path' not in self.conf_vars:
            self.conf_vars['html_static_path'] = []

        # Exclude static files, as they should not be processed.
        self.conf_vars['exclude_patterns'] += \
            self.conf_vars.get('html_static_path', [])
        self.conf_vars['exclude_patterns'] += \
            self.conf_vars.get('templates_path', [])

    def generate(self):
        """
        Read all the input files from the source directory, parse them, and
        output the results to the build directory.
        """
        # Check if requested format is supported.
        if self.builder not in Main.supported_builders:
            print("Requested builder not supported!", file=stderr)
            return 1

        self.file_ext, self.builder_class = Main.supported_builders[self.builder]

        # Check if destination path exists, otherwise create it.
        if not os.path.exists(self.dest_path):
            print("Making output directory...")
            os.mkdir(self.dest_path)
        self.dest_path = dir_path(self.dest_path)

        # Set-up reStructuredText directives
        spdirs.setup()
        custom_dirs.setup()

        # Load user configuration and extensions
        prev_cwd = os.getcwd()
        os.chdir(self.source_path)
        self.read_conf()
        self.sp_app = application.SphinxApp()
        for ext in self.conf_vars['extensions']:
            application.setup_extension(ext, self.sp_app)
        os.chdir(prev_cwd)

        # Set-up Table of Contents data
        self.build_global_toc()

        # Set-up index generator
        self.idx = index.IndexGenerator()

        # Iterate over files in source directory and save in [(path, content)]
        source_files = list()
        for root, dirs, files in os.walk(self.source_path):
            for dir in dirs:
                new_dir = os.path.join(self.dest_path, self.relative_path(root), dir)
                if not os.path.exists(new_dir):
                    os.mkdir(new_dir)
            for file in files:
                path = os.path.join(self.relative_path(root), file)
                try:
                    if any(file.endswith(suffix) for suffix in self.conf_vars['source_suffix']) \
                       and self.is_not_excluded(path):
                        content = self.parse_rst(path)
                        source_files.append((path, content))
                except FileNotFoundError as e:
                    print(f'File [{file}] not found:', e)
                except docutils.utils.SystemMessage as e:
                    print('DOCUTILS ERROR!', e)

        # Iterate over files and write to files.
        for path, content in source_files:
            self.write_rst(path, content)

        self.idx.build(os.path.join(self.dest_path, 'js'))
        self.copy_static_files()

        # TEMP
        temp_paths = ['css', 'js', 'fonts']
        for path in temp_paths:
            copy_tree(os.path.join('static', path),
                      os.path.join(self.dest_path, path), update=1)

        print("The generated documents have been saved in %s" % self.dest_path)
        return 0

    def parse_rst(self, path):
        """
        Parse a rst file.
        """
        src = os.path.join(self.source_path, path)
        html_path = path[:-4] + '.html'
        content = open(src).read()

        doctree = docutils.core.publish_doctree(
            content,
            source_path=src,
            settings_overrides={
                'src_dir': self.source_path,
                'dst_dir': self.dest_path
            }
        )
        for id in doctree.ids:
            application.id_map.update({id: html_path})

        return content

    def write_rst(self, path, content):
        """
        Parse a rst file and write its contents to a file.
        """
        src = os.path.join(self.source_path, path)
        html_path = path[:-4] + '.html'
        dest = os.path.join(self.dest_path, html_path)

        # Add epilog and prolog to source file.
        file_contents = '%s\n%s\n%s' % (
            self.conf_vars.get('rst_prolog', ''),
            content,
            self.conf_vars.get('rst_epilog', ''))

        # Read the rst file.
        settings = {
            'src_dir': self.source_path,
            'dst_dir': self.dest_path
        }
        doctree = docutils.core.publish_doctree(
            file_contents,
            source_path=src,
            settings_overrides=settings)

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
        self.idx.parse_file(content, title, html_path)

        # Write the document to a file.
        with open(dest, 'wb') as f:
            output = docutils.core.publish_from_doctree(
                doctree,
                destination_path=dest,
                writer=self.builder_class(),
                settings_overrides={
                    'toc': self.toc_navigation,
                    'src_dir': self.source_path,
                    'html_path': html_path,
                    'rel_base': os.path.relpath(self.dest_path, os.path.dirname(dest)),
                    'handlers': self.sp_app.get_handlers(),
                    'favicon': self.conf_vars.get('html_favicon', None),
                    'logo': self.conf_vars.get('html_logo', None),
                    'copyright': self.conf_vars.get('copyright', ''),
                    'html_style': self.conf_vars.get('html_style', None)
                })
            f.write(output)

    def is_not_excluded(self, path):
        """
        Check whether the supplied filename is not supposed to be excluded.
        """
        exclude_pats = self.conf_vars['exclude_patterns']
        if any(fnmatch.fnmatch(path, pattern) for pattern in exclude_pats):
            return False

        return True

    def build_global_toc(self):
        """
        Read and save the ToC from master_doc.
        """
        self.toc_navigation = list()

        # Open the file containing the ToC's
        master_doc = self.conf_vars.get('master_doc', 'index')
        src = None
        for suffix in self.conf_vars['source_suffix']:
            source_name = os.path.join(self.source_path, master_doc)
            if os.path.exists(source_name + suffix):
                src = source_name + suffix
                break

        if src is None:
            print("Invalid master_doc file specified in conf.py!", file=stderr)
            return

        doctree = docutils.core.publish_doctree(
            open(src, 'r').read(),
            source_path=src,
            settings_overrides={'src_dir': self.source_path})

        # Iterate and join ToC's.
        for tt in doctree.traverse(spdirs.toc_data):
            self.toc_navigation.append(tt)

    def copy_static_files(self):
        """
        Copy all the files from the static path to the destination path.
        """
        for path in self.conf_vars['html_static_path']:
            copy_tree(
                os.path.join(self.source_path, path),
                os.path.join(self.dest_path, '_static'),
                update=1)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description='SDG')
    arg_parser.add_argument('source_path', type=dir_path, help='The directory containing the RST files.')
    arg_parser.add_argument('-d', type=str, dest='destination_path', default='build', help='The directory to write '
                                                                                           'the output.')
    arg_parser.add_argument('-b', type=str, dest='builder', default="html", help='Builder used for the generator.')
    args = arg_parser.parse_args()

    print("Running SDG 0.0.1")
    main = Main(args.source_path, args.destination_path, args.builder)
    exit(main.generate())
