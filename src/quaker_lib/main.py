"""
TODO
"""

import os
import pkgutil
import fnmatch
import importlib
from pathlib import Path
from collections import defaultdict

from distutils.dir_util import copy_tree

from quaker_lib import index
from quaker_lib import directives
from quaker_lib import application
from quaker_lib import html5writer

from quaker_lib.page import Page
from quaker_lib.theme import Theme

from docutils.parsers.rst import Parser
from argparse import Namespace


class Main:
    """The central component of the program, from which everything else is called.

    Parameters
    ----------
    source_path : pathlib.Path
        The directory containing the source files.
    dest_path : pathlib.Path
        The directory to write the output.
    builder : str
        The builder used for the generator.
    """
    SKIP_TAGS = {'system_message', 'problematic'}

    # Mapping builder name to (output file extension, writer class) tuple
    supported_builders = {
        'html': ('html', html5writer.Writer)
    }

    def __init__(self, source_path, dest_path, builder):
        self.source_path = source_path
        self.dest_path = dest_path
        self.temp_path = dest_path.parent / 'tmp' / dest_path.name
        self.static_dest_path = dest_path / '_static'
        self.script_dest_path = self.static_dest_path / 'js'
        self.builder = builder
        self.source_parsers = {'.rst': Parser}

        self.sp_app = None
        self.theme = None
        self.file_ext = '.out'
        self.writer = None
        self.idx = None
        self.toc_navigation = []
        self.id_map = {}

        # Import and setup all directives.
        dir_path = Path(__file__).parent / 'directives'
        for _, module, _ in pkgutil.iter_modules([str(dir_path)]):
            module = importlib.import_module(f'quaker_lib.directives.{module}')
            module.setup()

        self.waiting = defaultdict(list)
        self.hierarchy = defaultdict(list)

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

        # Make sure source_suffix is a list.
        suffix = self.conf_vars['source_suffix']
        if suffix is None:
            self.conf_vars['source_suffix'] = ['.rst']
        elif isinstance(suffix, str):
            self.conf_vars['source_suffix'] = [suffix]

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

        # Add new source suffixes and parsers
        if len(self.sp_app.source_suffix) > 0:
            self.conf_vars['source_suffix'].append(*self.sp_app.source_suffix)
        self.source_parsers.update(self.sp_app.source_parsers)

        # Callback to extensions.
        for name, lst in self.sp_app.callbacks.items():
            if name == 'builder-inited':
                [callback(self.sp_app) for callback in lst]

        self.sp_app.env.config = Namespace(**self.sp_app.config)
        self.sp_app.env.docname = None
        self.sp_app.env.metadata = Namespace()
        self.sp_app.env.metadata.setdefault = lambda x, y: {}
        self.docutil_settings.update({
            'env': self.sp_app.env,
            'source_suffix': self.conf_vars['source_suffix']
        })

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

        # Create the destination directory if it does not exist.
        self.dest_path.mkdir(parents=True, exist_ok=True)

        # Load user configuration and extensions.
        self.load_extensions()

        # Set-up index generator and build the files.
        self.idx = index.IndexGenerator()
        self.build_files()

        # Set-up Table of Contents data and build the search index
        self.script_dest_path.mkdir(parents=True, exist_ok=True)
        self.build_global_toc()
        self.idx.build(self.temp_path, self.script_dest_path)

        # Copy the Javascript source files to the static directory in build.
        copy_tree(Path(__file__).parent / 'static' / 'js',
                  str(self.script_dest_path),
                  update=1)

        # Copy the directories from our theme directly to the dest folder.
        self.theme.copy_files(self.dest_path)

        # Copy static files from the source directly to the static dest folder.
        self.copy_static_files()

        # Delete the temporary build files.
        # TODO

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

                if path.suffix in self.conf_vars['source_suffix']:
                    page = Page(self, path)
                    page.parse()
                else:
                    page = None

                # Add the toc trees of the master doc page for the
                # creation of the sidebar.
                if (page is not None and
                        (str(path) == master_doc
                         or str(path.with_suffix('')) == master_doc)):
                    toc_node_type = directives.sphinx.toc_data
                    for toc_node in page.doctree.traverse(toc_node_type):
                        self.toc_navigation.append(toc_node)

        # Check if all the references are resolved.
        for ref_name, pages in self.waiting.items():
            for page in pages:
                print(f'Warning: {page.src} contains an unresolved '
                      f'reference "{ref_name}"')
                page.write()

    def is_excluded(self, path):
        """
        Check whether a file is not supposed to be excluded.

        Parameters
        ----------
        path : pathlib.Path
            The path to the file to be checked
        """
        exclude_pats = self.conf_vars['exclude_patterns']
        return any(fnmatch.fnmatch(path, pattern) for pattern in exclude_pats)

    def build_global_toc(self):
        """
        Read and save the ToC from master_doc.
        """
        with (self.script_dest_path / 'load_navbar.js').open('w') as f:
            f.write('document.getElementById("navigation-tree").innerHTML = `')

            for node in self.toc_navigation:
                node['numbered'] = False
                node['maxdepth'] = -1
                node['collapsedepth'] = 0
                for html in node.create_html(self.id_map, 'menu'):
                    f.write(html)

            f.write('`;')

    def copy_static_files(self):
        """
        Copy all the files from the static path to the destination path.
        """
        for path in self.conf_vars['html_static_path']:
            copy_tree(str(self.source_path / path),
                      str(self.static_dest_path),
                      update=1)

    def init_empty_project(self):
        """
        Initializes an empty project
        """
        path = Path(self.source_path)
        qs_path = Path(__file__).parent / '..' / 'quaker_lib' / 'quickstart'

        if not path.is_dir() or not path.exists():
            copy_tree(str(qs_path), str(path), update=1)
            print('Created an empty project in', self.source_path)
        else:
            print(f'Error: directory \'{path}\' already exists!')
