# -- General configuration ------------------------------------------------

# General information about the project.
project = 'My Project'
copyright = '2021, My Team'
author = 'My Author'
version = '0.1'
release = version

source_suffix = ['.rst']

extensions = []

exclude_patterns = [
    'build'
]

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

html_theme_path = ['..']
html_theme = 'quaker_theme'
html_style = 'css/bulma.min.css'
