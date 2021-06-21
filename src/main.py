"""
Main entrypoint of the program.
Call this script to invoke the generation of a static document/website.
"""

import os
import pkgutil
import fnmatch
import argparse
import importlib
from pathlib import Path
from collections import defaultdict

from distutils.dir_util import copy_tree

import index
import directives
import application
import html5writer

from page import Page
from theme import Theme


class Main:
    SKIP_TAGS = {'system_message', 'problematic'}

    # Mapping builder name to (output file extension, writer class) tuple
    supported_builders = {
        'html': ('html', html5writer.Writer)
    }

    def __init__(self, source_path, dest_path, builder):
        self.source_path = source_path
        self.dest_path = dest_path
        self.temp_path = dest_path.parent / 'tmp' / dest_path.name
        self.static_path = dest_path / '_static'
        self.builder = builder

        self.sp_app = None
        self.theme = None
        self.file_ext = '.out'
        self.writer = None
        self.idx = None
        self.toc_navigation = []

        # Import and setup all directives.
        dir_path = Path(__file__).parent / 'directives'
        for _, module, _ in pkgutil.iter_modules([str(dir_path)]):
            module = importlib.import_module(f'directives.{module}')
            module.setup()

        self.waiting = defaultdict(list)

        self.docutil_settings = {
            'src_dir': self.source_path,
            'dst_dir': self.dest_path,
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
        prev_cwd = Path.cwd()
        os.chdir(self.source_path)

        self.read_conf()
        self.sp_app = application.SphinxApp()
        for ext in self.conf_vars['extensions']:
            application.setup_extension(ext, self.sp_app)

        # Get path to theme
        self.theme = Theme(self.conf_vars.get('html_theme', 'quaker_theme'),
                           self.conf_vars.get('html_theme_path'),
                           self.conf_vars.get('templates_path', []))

        os.chdir(prev_cwd)

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

        # Set-up index generator and build the files.
        self.idx = index.IndexGenerator()
        self.build_files()

        # Set-up Table of Contents data
        self.build_global_toc()
        # Build search index.
        self.idx.build(self.temp_path, self.static_path / 'js')

        # Copy the directories from our theme directly to the dest folder.
        self.theme.copy_files(self.dest_path)
        self.copy_static_files()

        print(f'The generated documents have been saved in {self.dest_path}')

    def build_files(self):
        """Iterate over files in source directory and save in [(path, content)]
        """
        master_doc = self.conf_vars.get('master_doc', 'index')

        for root, _, files in os.walk(self.source_path):
            # Read, parse and write the source files to html.
            for file in files:
                path = self.relative_path(root) / file

                if self.is_excluded(path):
                    continue

                if path.suffix == '.rst':
                    page = Page(self, path)
                    page.parse(self)

                if str(path.with_suffix('')) == master_doc:
                    # Iterate and join ToC's.
                    ds = directives.sphinx
                    for queue in page.doctree.traverse(ds.toc_data):
                        self.toc_navigation.append(ds.TocTree.to_html(queue))

        # Check if all the references are resolved.
        for ref_name, pages in self.waiting.items():
            for page in pages:
                print(f'Warning: {page.src} contains an unresolved '
                      f'reference "{ref_name}"')
                page.write(self)

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

        path = self.static_path / 'js'
        path.mkdir(parents=True, exist_ok=True)

        with (path / 'load_navbar.js').open('w') as f:
            f.write('document.getElementById("navigation-tree").innerHTML = `')

            for html in self.toc_navigation:
                f.write(html)

            f.write('`;')

    def copy_static_files(self):
        """
        Copy all the files from the static path to the destination path.
        """
        for path in self.conf_vars['html_static_path']:
            copy_tree(str(self.source_path / path),
                      str(self.static_path),
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

    print("Running QuakerDocs 0.0.3")
    main = Main(args.source_path, args.build_path, args.builder)
    main.generate()
