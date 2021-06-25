"""
Functionality related to theme parsing.
"""

from distutils.dir_util import copy_tree
from configparser import ConfigParser
import os.path


class Theme:
    """
    Class for theme reading.
    """
    def __init__(self, theme_name, theme_path, templ_path):
        """
        Get all data related to a class.
        """
        self.theme_path = None
        self.inherit = None
        self.stylesheet = None

        # Get the paths to places where themes could be.
        src_file_path = os.path.abspath(os.path.dirname(__file__))
        dirs = [os.path.join(src_file_path, 'static')]

        if theme_path is not None:
            for cur_dir in theme_path:
                dirs.append(cur_dir)

        # Find the requested theme in the given directories.
        for current_dir in dirs:
            path = os.path.join(current_dir, theme_name)
            if os.path.exists(path) and os.path.isdir(path):
                self.theme_path = path
                break
        if self.theme_path is None:
            raise RuntimeError(f'Failed to find theme {theme_name}!')

        # Save additional paths to templates
        self.templates_path = [os.path.abspath(path) for path in templ_path] \
            if templ_path is not None else []

        # Parse the theme configuration.
        config = ConfigParser()
        config.read(os.path.join(self.theme_path, 'theme.conf'))

        inherit_name = config.get('theme', 'inherit', fallback=None)
        if inherit_name is not None:
            self.inherit = Theme(inherit_name, theme_path, [])
        self.stylesheet = config.get('theme', 'stylesheet', fallback=None)

    def get_template(self, filename='template.txt'):
        """
        Return the path to the template.
        """
        for current_dir in self.templates_path:
            path = os.path.join(current_dir, filename)
            if os.path.exists(path) and os.path.isfile(path):
                return path

        return self.get_file(filename)

    def get_file(self, filename):
        """
        Return the path to a file in the theme.
        """
        path = os.path.join(self.theme_path, filename)
        if os.path.exists(path) and os.path.isfile(path):
            return path
        if self.inherit is not None:
            return self.inherit.get_file(filename)

        return None

    def get_style(self):
        """
        Return the path to the stylesheet for this theme.
        """
        if self.stylesheet is not None:
            return self.stylesheet
        if self.inherit is not None:
            return self.inherit.get_style()

        return None

    def copy_files(self, dest_path):
        """
        Copy files from the theme to the static folder in the build directory.
        """
        if self.inherit is not None:
            self.inherit.copy_files(dest_path)

        if os.path.exists(os.path.join(self.theme_path, 'static')):
            copy_tree(os.path.join(self.theme_path, 'static'),
                      os.path.join(dest_path, '_static'),
                      update=1)
