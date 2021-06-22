Best Practices for AutoTest
========================================

.. deprecation_note:: /for-teachers/creating-automatic-tests/best-practices-in-autotest

This is a list of common questions and best practices for CodeGrade AutoTest.
This is by no means a complete list, if you have any other questions, please
consult the :ref:`AutoTest User Documenation <autotest-overview>` or the
CodeGrade Support Team at `support@codegrade.com <mailto:support@codegrade.com>`_.

When to use hidden steps?
---------------------------

For each step you create, you can toggle whether to hide it or not by clicking
the :fa:`eye` icon. By default all steps are visible. When you hide a step,
the name is still visible, but its details aren't. Also, when you're using
Continuous Feedback, hidden steps won't be run before the deadline. AutoTest
will automatically run all hidden steps within 30 minutes after the deadline.
There are some use cases to make your steps hidden:

1. **Performance heavy tests and Continuous Feedback**

You may sometimes have performance heavy tests. When giving your students
Continuous Feedback, you may want to hide these tests to speed up the process,
as hidden steps are not run until after the deadline.

2. **Not giving away all of your tests**

Sometimes you might want to have tests that students can see and other tests
that students cannot see. For example when having a simple test suite that
students can use to quickly tests their code and a deeper advanced test suite
that you will use to actually grade the code. With hidden tests, you can make
the deeper advanced tests hidden. You might also want to make sure you hide
your fixtures correctly, read more about how to do this
:ref:`here <best-practices-hide-fixtures>`.

Where do I compile students’ code (and how do I stop when compiling fails?)
----------------------------------------------------------------------------

We recommend two different ways to compile students' code. Which one to use
depends on the application.

1. **Using the per-student setup script**

If you want to use the compiled code in multiple categories, we recommend
using the per-student setup script for compiling. Either use a compilation script,
which you upload as a fixture, or input the compilation command directly in the
input field.

If you want to stop AutoTest when the compilation fails, you can do this in
the following way:

a. Create a compilation rubric category.
b. Create a new AutoTest level and add the compilation category in this level.
c. Use a Run Program step to check whether compilation was successful (e.g. by checking if the compiled files exist).
d. Save this category and create a new AutoTest level to put all your other test categories.
e. Set the *Only execute further levels* to 100%.

2. **Using a Run Program step and Checkpoint step**

If you only want to use the compiled code in one category (e.g. when every category has a different program), we recommend using a
Run Program step combined with a Checkpoint to compile the code.

a. Create a Run Program step with the compilation command.
b. Create a Checkpoint step right below the Run Program step and set it to 100%.

In this way, the category will stop testing if the Run Program step fails.

.. warning::
    Keep in mind that the state of AutoTest is reset to the state after the
    *per-student script* at the start of each category. So all your compiled
    files from method 2 are lost after the category finishes executing.


How to use weights and set rubric points when using a discrete rubric category?
--------------------------------------------------------------------------------

The final grade of an AutoTest run is not defined by the weights you set in
AutoTest, but by the amount of points a rubric level in a category has that is reached
by AutoTest.

To start setting the weights, first select the rubric calculation mode. Either
**minimum**, where a rubric category item will be chosen when the lower bound
is reached, or **maximum**, where a rubric category item will be chosen when
the upper bound is reached.

You want to use **maximum** when students need to pass all tests in an AutoTest
category, before they should get the maximum item in the rubric category.

Let's go over an example to make this more clear. This is the rubric category
we want to create tests for:

+------------------------------------+-------------------+---------------------+-----------------------+--------------------------+
| **Item name**                      | Nothing works (0) | Compiling works (1) | Simple tests work (5) | Advanced tests work (10) |
+------------------------------------+-------------------+---------------------+-----------------------+--------------------------+
| **Percentage range to reach item** | 0%-50%            | 50%-75%             | 75%-100%              | 100%                     |
+------------------------------------+-------------------+---------------------+-----------------------+--------------------------+

As you can see, the maximum mode is selected, as you only reach the last rubric
item (Advanced tests work) with 100% of passed tests.

+----------------------+---------------------------+------------+
| **Type**             | **Name**                  | **Weight** |
+----------------------+---------------------------+------------+
| Run Program          | Compile                   | 8          |
+----------------------+---------------------------+------------+
| Checkpoint           | Stop if compilation fails | \-         |
+----------------------+---------------------------+------------+
| IO Test (4 substeps) | Simple tests              | 4          |
+----------------------+---------------------------+------------+
| Capture Points       | Advanced tests            | 4          |
+----------------------+---------------------------+------------+

As you can see here, the *compile* step actually has the highest weight, but
will get the student the least amount of points. This is due to the fact that
you need a weight of *8* to get 50% in the rubric category, which in turn will
get you the *Compiling works* item.

Both the simple tests and advanced tests have a weight of 4, which is both
25% of the total amount of points achievable, which will make sure the right
rubric item is filled in.

How to manually adjust AutoTest grades?
-----------------------------------------

You can override the grade at all times by changing it in the grade input field.
If you rerun AutoTest, this overridden grade is preserved. If you only want
to adjust the grade down, you can also use a rubric category with negative weights
(so one item in the category with 0 points, and all the other items with less than 0 points).

How to install packages and third party software?
-----------------------------------------------------

Installing packages and third-party software can be done easily using the
*global setup script*. Either upload a bash script with installation commands
which you upload as a fixture, or input it directly in the input field. You can
install Ubuntu packages with ``sudo apt-get install -y PACKAGE_NAME``.

.. note::
    Always make sure to give the ``-y`` option to ``apt-get``, otherwise the package
    won't install.


How to assess style and structure?
-------------------------------------

You can assess style and structure by using a linter. Use the "Code Quality"
AutoTest step and choose a linter to run it on the code submitted by students.
This test will calculate its score based on the amount of comments the linter
generated. It is even possible to configure the penalties based on the severity
of the comment. Check out the :ref:`Code Quality documentation
<autotest-tests-code-quality>` for more information.

If your favorite linter is not listed, please do not hesitate to contact us at
`support@codegrade.com <mailto:support@codegrade.com>`_.

How to use a unit testing framework?
-----------------------------------------
You can use a unit testing framework by using one of the wrapper scripts that
we provide or by writing your own. The wrapper scripts write their results to
a file that is read by CodeGrade to get any output, error messages, and the
final score.

For many frameworks we have already written wrapper scripts to easily use them
in CodeGrade. Check out the :ref:`Unit Test documentation
<autotest-tests-unit-test>` for a list of supported frameworks, or contact us
at `support@codegrade.com <mailto:support@codegrade.com>`_ if your preferred
framework is not included so we can discuss what we can do!.

How to integrate existing grading scripts?
--------------------------------------------

Using an existing grading script in CodeGrade is straightforward, just slightly
modify the script so that it outputs a value between zero and one at the end,
upload it as a fixture and use a Capture Points test to execute the grading
script and capture the score.

.. note::
    If you need any help converting your existing grading scripts to CodeGrade
    grading scripts, feel free to contact us at
    `support@codegrade.com <mailto:support@codegrade.com>`_.

.. warning::
    It is important to note that rubric calculation and capture points might be a bit
    difficult to combine sometimes, especially when combining with IO tests
    too. In some cases it might be better to split the test script into multiple
    scripts (or use command line arguments), and use multiple 'run program' tests instead.

How do I combine AutoTest and manual function testing?
----------------------------------------------------------------------------

This is easily achieved by splitting your rubrics into multiple categories,
one category for the automated testing and one category for the manual testing.
In this way, AutoTest will fill in the automatic category and you can fill in
the manual category. This also has the advantage of a clear separation to your
students, making it easier for them to see which part is assessed automatically
and which part is assessed manually.

.. _best-practices-hide-fixtures:

How to hide fixtures?
-----------------------

Firstly, you can hide your fixtures in the User Interface. By default, fixtures
are hidden when you upload them. You can change the state by clicking the
:fa:`eye` icon.

However, this still means the code of students will be able to access these
fixtures on the AutoTest servers. You can limit this by using a special script.
You can read more about this :ref:`here <autotest-limit-student-access>`.

.. warning::
    If you're uploading solutions as fixtures you probably want to limit student
    access.

How to use IO tests with floating point numbers
---------------------------------------------------

Sometimes students might output numbers in a different format, or use a different
type of rounding. CodeGrade supplies a ``normalize_floats`` program in AutoTest
to solve this issue. You can use this in the following way: ``normalize_floats amount_of_decimals program_to_run``.

.. note::
    ``normalize_floats`` only transforms stdout and does not touch stderr.


How to let IO tests pass when the exit code is not 0
-------------------------------------------------------

IO tests fail by default if the exit code of the program is not 0. Sometimes,
however, you want IO tests to also pass with another exit code than 0. You
can simply fix this by appending ``|| true`` to your command, this will make
sure the exit code is always 0.

.. note::
    The "Input arguments" field of an IO step is appended to the command. This
    means that if it is not empty, this technique will likely not produce the
    expected results. To work around this case, add the ``|| true`` to the
    input arguments instead.

How to view AutoTest generated files
---------------------------------------

It may be desirable to inspect files that are generated during the run of an
AutoTest, such as compiled objects or IPython notebooks. By default generated
files are not saved, but they will be when you write them to the ``$AT_OUTPUT``
directory. The files will then be accessible through the "Autotest output"
section of the file browser in the Code Viewer.

.. _best-practices-submission-metadata:

How to access submission metadata from the tests
--------------------------------------------------

You may want to access some submission metadata in your tests, for example to
automatically subtract points when a student submitted after the deadline, or
you maybe you need to generate input for the tests but want it to be different
for each student. To enable this you first need to check the "Submission
information" checkbox in the "Advanced options" list at the bottom of the
AutoTest category editing window.

When you have done this, all steps in the current category will have an extra
environment variable named ``$CG_INFO`` defined. This variable contains a JSON
object with the following keys:

- ``deadline`` The deadline of this assignment.
- ``submitted_at`` The date and time the student submitted their work.
- ``result_id`` An identifier unique to this AutoTest result. This value changes
  every time the AutoTest is run, even if it is run multiple times for the same
  submission of the same student.
- ``student_id`` An identifier unique to the student for which the AutoTest is
  run. This value stays constant between runs of different submissions by the
  same student.

If you think it would be useful to have some extra data available, please do
not hesitate to contact us at `support@codegrade.com
<mailto:support@codegrade.com>`__ so we can discuss the options.

.. example:: subtracting points for late submissions

    You want to automatically subtract 1 point from the total rubric score for
    each day after the deadline, up to a maximum of 10 points subtracted.

    1. Set up a rubric category with 11 items ranging from -10 to 0.
    2. Create a new AutoTest category linked to the new rubric category, and
       check the  "Submission information" checkbox under "Advanced options".
    3. Add a "Capture points" step with an appropriate name and the following
       settings:

       * Program to test: ``python3.7 $FIXTURES/deadline.py`` (Note the use
         of ``python3.7`` instead of ``python3``)
       * Regex to match: ``\f``

    4. Upload the following script as a fixture with the name ``deadline.py``:

       .. code-block:: python
          :name: deadline-py

          import os
          import json
          import math
          import datetime

          ONE_DAY      = datetime.timedelta(days=1)

          cg_info      = json.loads(os.environ['CG_INFO'])
          deadline     = datetime.datetime.fromisoformat(cg_info['deadline'])
          submitted_at = datetime.datetime.fromisoformat(cg_info['submitted_at'])
          days_late    = math.ceil((submitted_at - deadline) / ONE_DAY)

          if days_late <= 0:
              print('submitted on time :)')
              print(1.0)
          elif days_late <= 10:
              print('{} days late'.format(days_late))
              print(1 - days_late / 10)
          else:
              print('very late, maximum penalty')
              print(0.0)

.. example:: generating random inputs

    You want to generate a list of 100 random numbers as inputs to the tests.

    1. Create a Python script named ``generate.py`` to generate the inputs. It
       uses the ``student_id`` key of ``$CG_INFO`` to seed the random number
       generator.  This has the consequence that the generated list of numbers
       stays the same between submissions of the same student. Upload the
       script created in step 1 as a fixture.

       .. code-block:: python
          :name: generate-py

          import os
          import json
          import random

          info = json.loads(os.environ['CG_INFO'])
          random.seed(info['student_id'])

          for _ in range(100):
              print(random.random())

    2. Create a run program step and pipe the generated numbers to the
       student's code with ``python3.7 generate.py | my_test_script``.