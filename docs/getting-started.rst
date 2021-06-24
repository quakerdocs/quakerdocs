Getting Started with QuakerDocs
================================

QuakerDocs is very easy to use, and you do not need a lot to get started!

Installation
------------

First of all to install the QuakerDocs application use the following command:

.. code-block:: bash

   pip install -e . --user

After running this command all the requirements are installed and you can immediately use the quaker command.

Quickstart
----------

To create an example quickstart directory, you need to use the following command:

.. code-block:: bash

   quaker --init <your_directory_name>

This command creates a directory with the :code:`conf.py`, :code:`index.rst` and :code:`page.rst` files.

Usage
-----

To use QuakerDocs to turn your reStructuredText files into a static webpage you need the follow these steps:

1. Open the directory containing your :code:`conf.py` in the terminal.

   .. code-block:: bash

      cd path/to/my/project

2. To convert your documentation files into a static webpage, run the following command.

   .. code-block:: bash

      quaker .

3. Change into the :code:`build/` directory, and start a webserver

   .. code-block:: bash

      cd ../build
      python3 -m http.server

4. To visit the generated documentation page visit :code:`localhost:8000` in your web browser.
