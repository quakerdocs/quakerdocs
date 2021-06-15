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
        # TODO: Location of themes?
        self.theme_path = theme_path
        config = ConfigParser()
        config.read(os.path.join(theme_path, 'theme.conf'))

        self.inherit = None
        inherit_name = config.get('theme', 'inherit', fallback=None)
        if inherit_name is not None:
            self.inherit = Theme(inherit_name)
        self.stylesheet = config.get('theme', 'stylesheet', fallback=None)

    def get_template(self):
        """
        Return the path to the template for the pages.
        """
        path = os.path.join(self.theme_path, 'template.txt')
        if os.path.exists(path) and os.path.isfile(path):
            ...  # Template exists and can be used.
        elif self.inherit is not None:
            path = self.inherit.get_template()
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
