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
    def __init__(self, theme_path):
        """
        Get all data related to a class.
        """
        self.theme_path = theme_path
        config = ConfigParser()
        config.read(os.path.join(theme_path, 'theme.conf'))

        inherit_name = config.get('theme', 'inherit', fallback=None)
        if inherit_name is not None:
            self.inherit = Theme(inherit_name)
        self.stylesheet = config.get('theme', 'stylesheet')

    def get_template(self):
        """
        Return the path to the template for the pages.
        """
        return os.path.join(self.theme_path, 'template.txt')

    def copy_files(self, dest_path):
        """
        Copy files from the theme to the static folder in the build directory.
        """
        copy_tree(os.path.join(self.theme_path, 'static'),
                  os.path.join(dest_path, '_static'),
                  update=1)
