.. _autotest-categories:

Categories
==============

.. deprecation_note:: /user-reference/autotest-general/autotest-categories-levels#categories

Within a :ref:`level <autotest-levels>` you can create a Category. Each Category
has to be connected to a Rubric Category (see :ref:`here
<autotest-setup-rubric-calculation>` for information how this rubric will be
filled in). By doing this, AutoTest is feedback oriented. We encourage teachers
to create meaningful Rubric Categories and think about how to group their tests
accordingly. By grouping tests into AutoTest Categories that are connected to a
Rubric Category, this also means that students know where tests belong and how
they got their grade for an assignment.

Setup
------------------------------

Press the **Add Category** button inside a level to create a new Category within
your AutoTest configuration.

Firstly, select the Rubric Category you want to connect it to.

.. note::
    Make sure to create your Rubric Categories before creating your AutoTest
    Categories.

Next, you can add tests to this category. You have several different types of
tests you can add to this.

- **IO Tests** for simple input/output tests.
- **Run Program Tests** to run a program and check if the program exited
  successfully.
- **Capture Points Tests** to run a custom test program (such as a unit test)
  which captures a number between 0 and 1 and converts this to an amount of
  points.
- **Check Points**, which check if the percentage of points gotten before this
  special test is high enough to continue with the tests after the Check Points
  test. This makes it possible to have certain tests only execute if tests
  before it were successful.
- **Unit Test** for integration with unit testing frameworks that support JUnit
  compatible XML output.

Advanced options
~~~~~~~~~~~~~~~~

Each category has a few settings that will be active for all tests within the
category.

- **Timeout per step**: When a single test in the category is taking longer
  than this amount of seconds, the process is killed, the status of the test
  will be set to :fa:`exclamation-triangle` **timeout** and no points are given
  for this test.

  It is preferred to keep this value low -- while giving the student's code
  enough time to run of course! -- so that code that contains an accidental
  infinite loop will not fill up the AutoTest queue.
- **Network disabled**: Disable the network while the tests in this category
  are running.
- **Submission information environment variables**: Include information about
  the submission being tested in the ``$CG_INFO`` enfironment variable. The
  value is a JSON object with the following keys:

  - ``deadline`` The deadline of this assignment.
  - ``submitted_at`` The date and time the student submitted their work.
  - ``result_id`` An identifier unique to this AutoTest result. This value changes
    every time the AutoTest is run, even if it is run multiple times for the same
    submission of the same student.
  - ``student_id`` An identifier unique to the student for which the AutoTest is
    run. This value stays constant between runs of different submissions by the
    same student.

  See the :ref:`AutoTest Best Practices <best-practices-submission-metadata>`
  guide for some concrete examples of how this can be used.

Running
--------------------

When AutoTest is executed, each Category starts with a fresh snapshot of the
environment setup. This means that Categories run independently of each other.
Tests within the Category are executed in order.
