.. _autotest-levels:

Levels
===========

.. deprecation_note:: /user-reference/autotest-general/autotest-categories-levels#levels

After setting up the AutoTest environment it's time to actually create some
tests. To do this, you first have to create an AutoTest Level. This is done by
pressing the **Add Level** button.

A Level contains :ref:`Categories <autotest-categories>`. These Categories are
connected to a Rubric Category and contain the actual tests.

The Categories within a Level are executed independent of each other and
could be executed concurrently. This means that there is no order between
Categories within a level (the tests within a Category are executed in order).

For most use cases one level is enough to do all your testing with.

Advanced use cases
--------------------

There is the possibility, however, to create multiple levels. This can be
done, for example, if you only want to run certain categories if other categories
(in another level) get a certain percentage of points. After adding a
new level you can set this percentage in the footer of the set above.

Levels are executed in order, and not concurrently.
