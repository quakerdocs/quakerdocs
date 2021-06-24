Getting Started with QuakerDocs
================================

QuakerDocs is very easy to use, and you do not need a lot to get started!

Installation
------------

First of all to install the QuakerDocs application use the following command:

.. code-block:: bash

   pip install .

After running this command all the requirements are installed and you can immediately use the quaker command.

Quickstart
----------

To create an example quickstart project in a directory, you can use the following command:

.. code-block:: bash

   quaker --init <your_directory_name>

This command creates a directory with some of the necessary files to get you started such as :code:`conf.py`, and :code:`index.rst`.

Usage
-----

To use QuakerDocs to turn your RST of Markdown files into static webpages you need the follow these steps:

1. Open the directory containing your :code:`conf.py` in the terminal.

   .. code-block:: bash

      cd path/to/my/project/

2. To convert your documentation files into static webpages, run the following command.

   .. code-block:: bash

      quaker .

3. Change into the :code:`build/` directory, and start a webserver.

   .. code-block:: bash

      cd build/
      python3 -m http.server

4. To visit the generated documentation page visit :code:`localhost:8000` in your web browser.
