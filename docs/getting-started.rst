Getting Started with QuakerDocs
================================

QuakerDocs is very easy to use, and you do not need a lot to get started!
To get started, you only need a configuration file written in Python called :code:`conf.py`, and one or more files containing your documentation called :code:`<your_file_name>.rst`.
An example can be downloaded from `here <www.google.com>`_ .

Installation
------------

First of all clone the git repository:

.. code-block:: bash

    git clone ssh://git@gitlab-fnwi.uva.nl:1337/lreddering/pse-documentation-generator.git

When all the files have been cloned, run :code:`pip install -r requirements.txt` to install all the required dependencies for quaker to work.
When this is done, just run :code:`make install` to install quaker to your system.

Usage
-----

To use QuakerDocs to turn your reStructuredText files into a static webpage you need the follow these steps:

1. Open the directory containing your :code:`conf.py` in the terminal.

   .. code-block:: bash

      cd path/to/my/project

2. To convert your documentation files into a static webpage, run the following command.

   .. code-block:: bash

      quaker . -d build

3. (Change into the build directory, and start a webserver)

   .. code-block:: bash

       python3 -m http.server

4. To visit the generated documentation page visit localhost:8000 in your web browser.
