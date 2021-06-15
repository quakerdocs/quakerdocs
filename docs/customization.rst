Customize your documentation with Quaker Docs
==============================================

QuakerDocs supports customizing your own documentation build with a
configuration file. This file is named ``conf.py`` and is found in the /docs
directory.

Provided stylesheets
~~~~~~~~~~~~~~~~~~~~~~

We provide you with the following 6 stylesheets which are bulma.io compatible.
Thanks to https://jenil.github.io/bulmaswatch/ for the provided stylesheets.

.. |bulma-min-png| raw:: html

    <figure class="image is-16by9">
    <img src="_static/_images/bulma.min.png">
    </figure>

.. |bulma-min-classy-png| raw:: html

    <figure class="image is-16by9">
    <img src="_static/_images/bulma.min-classy.png">
    </figure>

.. |bulma-min-css-png| raw:: html

    <figure class="image is-16by9">
    <img src="_static/_images/bulma.min-css.png">
    </figure>

.. |bulma-min-dark-png| raw:: html

    <figure class="image is-16by9">
    <img src="_static/_images/bulma.min-dark.png">
    </figure>

.. |bulma-min-jet-png| raw:: html

    <figure class="image is-16by9">
    <img src="_static/_images/bulma.min-jet.png">
    </figure>

.. |bulma-min-night-png| raw:: html

    <figure class="image is-16by9">
    <img src="_static/_images/bulma.min-night.png">
    </figure>

.. |bulma-min-red-png| raw:: html

    <figure class="image is-16by9">
    <img src="_static/_images/bulma.min-red.png">
    </figure>


Bulma.min
-----------

.. code-block:: python

    html_style = 'css/bulma.min.css'

|bulma-min-png|

Bulma.min-classy
------------------

.. code-block:: python

    html_style = 'css/bulma.min-classy.css'

|bulma-min-classy-png|

Bulma.min-dark
------------------

.. code-block:: python

    html_style = 'css/bulma.min-dark.css'

|bulma-min-dark-png|

Bulma.min-jet
------------------

.. code-block:: python

    html_style = 'css/bulma.min-jet.css'

|bulma-min-jet-png|

Bulma.min-night
------------------

.. code-block:: python

    html_style = 'css/bulma.min-night.css'

|bulma-min-night-png|

Bulma.min-red
------------------

.. code-block:: python

    html_style = 'css/bulma.min-red.css'

|bulma-min-red-png|

Adding your own css
~~~~~~~~~~~~~~~~~~~~~

You can always add more stylesheets to the already provided stylesheets by
visiting `Bulmaswatch <https://jenil.github.io/bulmaswatch/>`_ . Just download the style and
give a shoutout to bulma afterwards on `Twitter <https://twitter.com/>`_ .

Add the css file to
``static/css`` and change the html_style to the given name.
