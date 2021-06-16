"""
Main entrypoint of the program.
Call this script to invoke the generation of a static document/website.
"""

import os
import pkgutil
import fnmatch
import argparse
import importlib
from sys import stderr

from pathlib import Path
from distutils.dir_util import copy_tree
import docutils.core
import docutils.writers
from docutils import nodes
import docutils.parsers.rst
import docutils.writers.html5_polyglot

import index
import application
import html5writer
from theme import Theme
import directives

SKIP_TAGS = {'system_message', 'problematic'}


class Main:
    """
    Class for controlling the main functionality of the program.
    """
    # Mapping builder name to (output file extension, writer class) tuple
    supported_builders = {
        'html': ('html', html5writer.Writer)
    }

    def __init__(self, source_path, build_path, builder):
        self.source_path = source_path
        self.build_path = build_path
        self.dest_path = build_path / 'html'
        self.builder = builder
        self.sp_app = None
        self.theme = None
        self.file_ext = '.out'
        self.writer = None
        self.idx = None
        self.toc_navigation = list()

        # Import and setup all directives.
        dir_path = Path(__file__).parent / 'directives'
        for _, module, _ in pkgutil.iter_modules([str(dir_path)]):
            module = importlib.import_module(f'directives.{module}')
            module.setup()

        self.docutil_settings = {
            'src_dir': self.source_path,
            'dst_dir': self.dest_path
        }

        self.conf_vars = {
            'exclude_patterns': [],
            'html_static_path': [],
        }

    def relative_path(self, path):
        """
        Get the path of a source directory relative to the source file.
        """
        return Path(path).relative_to(self.source_path)

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
        with open('conf.py') as conf_file:
            exec(conf_file.read(), global_vars, conf_vars)
        self.conf_vars.update(conf_vars)

        # NOTE: this shouldn't be needed.
        # suffix = self.conf_vars['source_suffix']
        # if isinstance(suffix, str):
        #     self.conf_vars['source_suffix'] = [suffix]

        # self.conf_vars['source_suffix']=set(self.conf_vars['source_suffix'])

        # Exclude static files, as they should not be processed.
        self.conf_vars['exclude_patterns'] += \
            self.conf_vars.get('html_static_path', [])
        self.conf_vars['exclude_patterns'] += \
            self.conf_vars.get('templates_path', [])

    def load_extensions(self):
        """
        Load user configuration and extensions.
        """
        prev_cwd = os.getcwd()
        os.chdir(self.source_path)
        self.read_conf()
        self.sp_app = application.SphinxApp()
        for ext in self.conf_vars['extensions']:
            application.setup_extension(ext, self.sp_app)
        os.chdir(prev_cwd)

        # Get path to theme
        self.theme = Theme(self.conf_vars.get('html_theme', 'quaker_theme'),
                           self.conf_vars.get('html_theme_path'))

    def generate(self):
        """
        Read all the input files from the source directory, parse them, and
        output the results to the build directory.
        """
        # Check if requested format is supported.
        if self.builder not in Main.supported_builders:
            raise NotImplementedError("Requested builder not supported!")

        self.file_ext, self.writer = Main.supported_builders[self.builder]

        # Make the destination directory if it does not exist.
        self.dest_path.mkdir(parents=True, exist_ok=True)

        # Load user configuration and extensions.
        self.load_extensions()

        # Set-up Table of Contents data
        self.build_global_toc()

        # Set-up index generator and build the files.
        self.idx = index.IndexGenerator()
        self.build_files()

        # Build index.
        self.idx.build(self.build_path, self.dest_path / 'js')

        # Copy the directories from our theme directly to the dest folder.
        self.theme.copy_files(self.dest_path)
        self.copy_static_files()

        print('The generated documents have been saved in %s' % self.dest_path)

    def build_files(self):
        """Iterate over files in source directory and save in [(path, content)]
        """
        for root, dirs, files in os.walk(self.source_path):
            # Recreate the source directories.
            for cur_dir in dirs:
                new_dir = self.dest_path / self.relative_path(root) / cur_dir
                if not new_dir.exists():
                    new_dir.mkdir()

            # Read, parse and write the source files to html.
            for file in files:
                path = self.relative_path(root) / file

                if self.is_excluded(path):
                    continue

                try:
                    if path.suffix == '.rst':
                        self.write_rst(*self.parse_rst(path))
                except FileNotFoundError as err:
                    print(f'File [{file}] not found:', err)
                except docutils.utils.SystemMessage as err:
                    print('DOCUTILS ERROR!', err)

    def parse_rst(self, path):
        """
        Parse a rst file.
        """
        src = self.source_path / path
        html_path = path.with_suffix('.html')

        with open(src) as file:
            content = file.read()

        doctree = docutils.core.publish_doctree(
            content,
            source_path=str(src),
            settings_overrides=self.docutil_settings
        )

        for section_id in doctree.ids:
            application.id_map.update({section_id: html_path})

        return src, html_path, content

    def write_rst(self, src, html_path, content):
        """
        Parse a rst file and write its contents to a file.
        """
        # src = self.source_path / path
        # html_path = path.with_suffix('.html')
        dest = self.dest_path / html_path

        # Add epilogue and prolog to source file.
        file_contents = '%s\n%s\n%s' % (
            self.conf_vars.get('rst_prolog', ''),
            content,
            self.conf_vars.get('rst_epilog', ''))

        # Read the rst file.
        doctree = docutils.core.publish_doctree(
            file_contents,
            source_path=str(src),
            settings_overrides=self.docutil_settings)

        # Get the page metadata.
        metadata = directives.metadata.get_metadata(doctree)
        if metadata.ignore:
            return

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
        content = ' '.join(n.astext() for n in doctree.traverse(
                           lambda n: isinstance(n, nodes.Text)))
        self.idx.add_file(content, title, html_path, metadata.priority)

        # Write the document to a file.
        with open(dest, 'wb') as file:
            output = docutils.core.publish_from_doctree(
                doctree,
                destination_path=dest,
                writer=self.writer(),
                settings_overrides={
                    'toc': self.toc_navigation,
                    'template': self.theme.get_file('template.txt'),
                    'stylesheet': os.path.join(
                        '_static', self.conf_vars.get('html_style',
                                                      self.theme.get_style())),
                    'src_dir': self.source_path,
                    'html_path': html_path,
                    'embed_stylesheet': False,
                    'rel_base': os.path.relpath(self.dest_path, dest.parent),
                    'handlers': self.sp_app.get_handlers(),
                    'favicon': self.conf_vars.get('html_favicon', None),
                    'logo': self.conf_vars.get('html_logo', None),
                    'copyright': self.conf_vars.get('copyright', ''),
                    'html_style': self.conf_vars.get('html_style', None)
                })
            file.write(output)

    def is_excluded(self, path):
        """
        Check whether the supplied filename is not supposed to be excluded.
        """
        exclude_pats = self.conf_vars['exclude_patterns']
        return any(fnmatch.fnmatch(path, pattern) for pattern in exclude_pats)

    def build_global_toc(self):
        """
        Read and save the ToC from master_doc.
        """
        self.toc_navigation = list()

        # Open the file containing the ToC's
        master_doc = self.conf_vars.get('master_doc', 'index')
        master_source = None
        for suffix in ['.rst']:
            src = self.source_path / (master_doc + suffix)
            if src.exists():
                master_source = src
                break
        else:
            print("Invalid master_doc file specified in conf.py!", file=stderr)
            return

        doctree = docutils.core.publish_doctree(
            master_source.open().read(),
            source_path=str(master_source),
            settings_overrides={'src_dir': self.source_path})

        # Iterate and join ToC's.
        for current_toc in doctree.traverse(directives.sphinx.toc_data):
            self.toc_navigation.append(current_toc)

    def copy_static_files(self):
        """
        Copy all the files from the static path to the destination path.
        """
        for path in self.conf_vars['html_static_path']:
            copy_tree(str(self.source_path / path),
                      str(self.dest_path / '_static'),
                      update=1)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description='QuakerDocs')
    arg_parser.add_argument('source_path', type=Path,
                            help='The directory containing the RST files.')
    arg_parser.add_argument('-d', type=Path, dest='build_path',
                            default='build',
                            help='The directory to write the output.')
    arg_parser.add_argument('-b', type=str, dest='builder', default="html",
                            help='Builder used for the generator.')
    args = arg_parser.parse_args()

    print("Running QuakerDocs 0.0.2")
    main = Main(args.source_path, args.build_path, args.builder)
    main.generate()
