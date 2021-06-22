Configure with QuakerDocs
=========================

QuakerDocs supports configuring your own documentation build with a
configuration file. This file is named `conf.py` and is found in the
root of your configuration directory.

Extensions
----------

Add extension module names here, as strings. Quaker will look for your
extensions in your system path. To add a new folder containing
extensions to the path, you can use python.

Templates
---------

Add any paths that contain templates here, relative to the configuration
directory.

``` {code-block} python
templates_path = ['my_templates']
```

Source suffix
-------------

The suffix(es) of source filenames to be parsed as reStructuredText. You
can specify multiple suffix as a list of string:

``` {code-block} python
source_suffix = ['.rst', '.md']
```

Master document
---------------

The master 'table of contents' document. This is the document that
Quaker will use to generate the table of contents that is shown in the
sidebar. It will parse the master document and retrieve all table of
contents on that page. You can specify the master document of your
documentation webpage:

``` {code-block} python
master_doc = 'index'
```

Information about your project
------------------------------

General information about the project.

``` {code-block} python
project = 'My Project'
copyright = '2021, My Team'
author = 'My Name'
```

Version
-------

The version info for the project you're documenting, used in various
other places throughout the built documents.

``` {code-block} python
# The short X.Y version.
version = '0.1'
# The full version, including alpha/beta/rc tags.
release = version
```

Exclude patterns
----------------

List of patterns, relative to source directory, that match files and
directories to ignore when looking for source files. This patterns also
affects `html_static_path`.

``` {code-block} python
exclude_patterns = ['build/*']
```

Options for HTML
----------------

### HTML theme path

Specify the path to the directory containing custom template files,
relative to the configuration directory.

``` {code-block} python
html_theme_path = ['my_templates']
```

### HTML theme

The theme to use for HTML pages.

``` {code-block} python
html_theme = 'quakerdocs'
```

### HTML static path

Add any paths that contain custom static files (such as style sheets)
here, relative to this directory. They are copied to the \_static
directory in the build directory after the builtin static files, so a
file named "default.css" will overwrite the builtin "default.css".

``` {code-block} python
html_static_path = ['_static']
```

### HTML favicon

Add the path and filename of the favicon you want to use for the
webpage.

``` {code-block} python
html_favicon = '_static/_images/favicon.ico'
```

### HTML logo

Add the path and filename of the logo you want to use for the webpage.

``` {code-block} python
html_logo = '_static/_images/logo.png'
```
