QuakerDocs
==========================

QuakerDocs is a modern and reliable static documentation generator. It
was designed from the ground up to replace older documentation
generators. It generates a fully static web page with your
documentation, so it can work without a server. Some of the features
that QuakerDocs has are:

-   Fast generation of a static website
-   Write documentation using reStructuredText
-   Super-fast live search
-   Handy bookmarking system
-   Easily configurable
-   Only takes one command!

Getting Started with QuakerDocs
===============================

QuakerDocs is very easy to use, and you do not need a lot to get
started! To get started, you only need a configuration file written in
Python called `conf.py`, and one or more files containing your
documentation called `<your_file_name>.rst`.

Installation
------------
You can install QuakerDocs from PyPI as follows:

``` {.bash}
$ pip install quaker
```

Usage
-----

To use QuakerDocs to turn your RST or Markdown files into a static
webpage you need the follow these steps:

1.  Open the directory containing your `conf.py` in the terminal.

    ``` {.bash}
    cd path/to/my/project
    ```

2.  To convert your documentation files into a static webpage, run the
    following command.

    ``` {.bash}
    quaker . -d build
    ```

3.  (Change into the build directory, and start a webserver)

    ``` {.bash}
    python3 -m http.server
    ```

4.  To visit the generated documentation page visit localhost:8000 in
    your web browser.