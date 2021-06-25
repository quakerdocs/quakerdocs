import os
import sys
from datetime import date

sys.path.insert(0, os.path.abspath('./_ext'))

# -- General configuration ------------------------------------------------
extensions = [
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

source_suffix = ['.rst']

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'QuakerDocs'
copyright = str(date.today().year) + ', QuakerDocs'
author = 'PSE Team D'

# The short X.Y version.
version = 'v0.3'
# The full version, including alpha/beta/rc tags.
release = version

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = [
]

# The weight of words in the title relative to regular content, for building
# the search index.
title_weight = 5

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

html_theme_path = ['..']
html_theme = 'quaker_theme'
# html_style = 'css/bulma.min-classy.css'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_favicon = '_static/_images/favicon.ico'
html_logo = '_static/_images/logo.png'
