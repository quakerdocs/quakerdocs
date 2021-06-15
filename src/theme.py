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
    def __init__(self, theme_name, theme_path):
        """
        Get all data related to a class.
        """
        # Get the paths to places where themes could be.
        dirs = theme_path if theme_path is not None else [
            os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
        ]

        for dir in dirs:
            path = os.path.join(dir, theme_name)
            if os.path.exists(path) and os.path.isdir(path):
                self.theme_path = path
                break
        if self.theme_path is None:
            print("Failed to find specified theme %s!" % theme_name)
            return None

        config = ConfigParser()
        config.read(os.path.join(self.theme_path, 'theme.conf'))

        self.inherit = None
        inherit_name = config.get('theme', 'inherit', fallback=None)
        if inherit_name is not None:
            self.inherit = Theme(inherit_name, theme_path)
        self.stylesheet = config.get('theme', 'stylesheet', fallback=None)

    def get_file(self, filename):
        """
        Return the path to a file in the template.
        """
        path = os.path.join(self.theme_path, filename)
        if os.path.exists(path) and os.path.isfile(path):
            ...  # Template exists and can be used.
        elif self.inherit is not None:
            path = self.inherit.get_file(filename)
        else:
            path = None

        return path

    def get_style(self):
        """
        Return the path to the stylesheet for this theme.
        """
        if self.stylesheet is not None:
            return self.stylesheet
        elif self.inherit is not None:
            return self.inherit.get_style()
        else:
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
