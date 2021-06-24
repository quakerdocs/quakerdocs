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
started!

Installation
------------

First of all, make sure you have Clang and the LLVM wasm-compiler installed.

For example, on Ubuntu:

``` {.bash}
apt install clang lld
```

Then, to install the QuakerDocs application use the following command:

``` {.bash}
pip install quaker
```

After running this command all the requirements are installed and you can
immediately use the quaker command.

Quickstart
----------

To create an example quickstart project in a directory, you can use the
following command:

``` {.bash}
quaker --init <your_directory_name>
```

This command creates a directory with some of the necessary files to get
you started such as `conf.py`, and `index.rst`.

Usage
-----

To use QuakerDocs to turn your RST or Markdown files into static
webpages you need the follow these steps:

1.  Open the directory containing your `conf.py` in the terminal.

    ``` {.bash}
    cd path/to/my/project/
    ```

2.  To convert your documentation files into static webpages, run the
    following command.

    ``` {.bash}
    quaker .
    ```

3.  Change into the `build/` directory, and start a webserver.

    ``` {.bash}
    cd build/
    python3 -m http.server
    ```

4.  To visit the generated documentation page visit `localhost:8000` in
    your web browser.
