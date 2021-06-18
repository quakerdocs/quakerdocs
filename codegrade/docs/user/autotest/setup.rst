.. _autotest-setup:

Setup
==================

.. deprecation_note:: /user-reference/autotest-general/autotest-setup

To make CodeGrade AutoTest as flexible as possible, it is possible to customize
the complete environment the tests are run in. Each separate assignment that
makes use of AutoTest runs on its own Virtual Server in the cloud, to which you
have superuser rights and network access during the setup phase. Every server on
official CodeGrade instances runs with the latest LTS version of Ubuntu, which
is **Ubuntu 18.04.2 LTS**.

After the Setup Phase is finished, a snapshot is created which is used to
initialize the containers used to run the actual tests on the student
submissions. The Setup Phase consists of the default installed software,
fixtures (the location of the fixtures directory is random for every category
and setup script to make it more virtually impossible for students to guess the
location and changes. The location is stored in the ``$FIXTURES`` environment
variable) and setup script.

.. warning::
    Setup scripts and other scrips (fixtures) that are executed have to use
    **Unix Line Endings (LF)** and **not** Windows Line Endings (CRLF)!

There are multiple options for setting up your environment, which makes AutoTest
easy to use for simple cases yet very flexible for all advanced cases.

Default Installed Software
---------------------------

Each AutoTest VPS environment comes with pre-installed software that is
commonly used for testing and running student submissions. This body of software
is sufficient for most cases, which allows you to skip manually further setting
up the environment.

The following software is automatically installed in all environments, all
versions, except for Python, are lower bounds, as all packages are always
updated to the latest version shipped by Ubuntu:

- Python 2.7 *(with pip)*
- Python 3.6 *(with pip3)*
- Python 3.7 *(with pip3)*
- Java 8 *(openjdk-8-jdk)*
- Java 11 *(openjdk-11-jdk)*
- Jupyter/IPython
- Mono *(6.4)*
- Node *(JavaScript 8.10)*
- Octave *(4.2.2)*
- R *(r-base 3.4)*
- C/C++ *(gcc 7 and clang 6 as compilers)*
- Go *(golang 1.10)*
- Git
- Maven
- Flake8
- Numpy *(for Python2, Python3.6 and Python3.7)*
- SciPy *(for Python2, Python3.6 and Python3.7)*
- Check *(unit test framework for C)*

Read the following sections to find out about extending this environment with
other required software.

Unit testing wrapper scripts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In addition to the software listed above, CodeGrade provides custom wrapper
scripts for popular unit testing frameworks to make integration with Autotest
a breeze. See :ref:`the Tests chapter <auto-test-supported-frameworks>`
for a list of supported unit testing frameworks.

.. _at-result-visibility:

Result visibility
----------------------

When a student uploads, AutoTest immediately runs on the handed in submission.
You can choose whether you want the student to directly be able to view the
AutoTest result (known as :ref:`Continuous Feedback <cont-feedback>`)
or that the student can only view the result when the assignment is set to
"Done" (just like with any other feedback).

The AutoTest rubric categories will be filled in automatically and directly in
either case if you have not created any hidden steps.

.. warning::
    If you have created hidden steps, AutoTest will be run again automatically
    within 30 minutes after the deadline, where the hidden steps are also executed.
    Before the deadline, hidden steps are never executed.

.. _autotest-setup-rubric-calculation:

Rubric calculation
-------------------

The rubric calculation setting determines how (discrete) rubric categories will
be filled-in.

Discrete Categories
~~~~~~~~~~~~~~~~~~~~

There are two modes to fill in discrete rubric categories:

1. **Minimum**: A category's item will be chosen when the lower bound of this
   item is reached (e.g. when a category has 4 items and 75% of the tests
   succeed, the maximum item is filled in).
2. **Maximum**: A category's item will be chosen when the upper bound of this
   item is reached (e.g. you need 100% passed tests to have the maximum item
   filled in).

.. note::

    The percentages of the items in a category are independent of the amount of
    points given to them. E.g. if you have 4 items, item 1 is always 0%-25%,
    item 2 is 25%-50% and so forth.

Continuous Categories
~~~~~~~~~~~~~~~~~~~~~

Continuous rubric categories are filled in one way, this means this setting will
have no influence on rubric calculation for this type of rubric category. The
percentage achieved in the AutoTest level will also be the percentage achieved
in the continuous rubric category.

.. example::

   You have a continuous rubric category with a maximum of 5 points, and an
   AutoTest level with a maximum of 10 points. If a user achieves 7 AutoTest
   points for this level, in the continuous rubric category the student will
   receive :math:`5 \times \frac{7}{10} = 3.5` points.

Running a teacher's revision
----------------------------

When the preferred revision is set to "Teacher", and a teacher's revision is
available for a submission, AutoTest is run against the teacher revision
instead of the code submitted by the student. If no teacher's revision is
present AutoTest will be run against the code of the student.

This can be useful if a student has made a tiny mistake in their code -- for
example a misplaced punctuation mark -- that causes the majority of the tests
to fail. The teacher can correct this mistake and run the tests again to see
what the score of this student would have been if such a mistake weren't made.

After the teacher has made their changes, the AutoTest should be manually
restarted if it has already started or finished, to make it run against the
teacher's revision. You can restart an AutoTest by going to a result, clicking
on the arrow next to the state of the result, and selecting "Restart this
result".

Uploading fixtures
--------------------

Fixtures can be optionally uploaded to the AutoTest VPS. Fixtures are files you
can upload prior to the test, which will be available in every separate test
container. Use cases are files used as setup script (see next section), unit
tests, custom software to run or install and test input.

Select the fixtures to be uploaded and submit these to upload. A list of
previously uploaded fixtures can be found above the upload dialog and managed
here too.

.. warning::
    Archives are **not** automatically extracted when uploading fixtures. This
    makes it possible to use *unextracted* archives as fixtures too. Use the
    commands ``tar xfvz $FIXTURES/ARCHIVE.tar.gz`` or
    ``unzip $FIXTURES/ARCHIVE.zip`` to extract archives manually. Be careful
    with the permissions, we recommend running ``chown -R codegrade:codegrade
    $FIXTURES/dir`` and ``chmod -R 750 $FIXTURES/dir`` after extracting.

.. _autotest-limit-student-access:

Limiting student access
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
It is sometimes desirable to limit student access to fixtures or to limit the
visibility of your uploaded fixtures. For instance if one of your fixtures is a
solution to the assignment you use to test student submissions against.

We offer multiple means of limiting undesirable student access to fixtures.
Firstly, the path to the fixtures is randomly generated for each category and
thus only accessible using the ``$FIXTURES`` environment variable. This makes it
harder for students to access the path, but not impossible.

A way to further limit student permissions in the ``$FIXTURES`` folder is to
execute student code with the ``become_nobody`` command. When executed in this
mode, students will have no permissions to read from the ``$FIXTURES`` folder.
They will have permissions in the ``$STUDENT`` folder, which is the current
directory in which student submission files are accessible, to read and
execute.

.. note::
    Copying files from the ``$FIXTURES`` directory to the ``$STUDENT`` directory
    with the ``cp`` or ``mv`` commands will **not** change permissions on these
    files, and the ``nobody`` user will **not** be able to read them. Use
    ``chmod 755 <FILE>`` to properly set these or use the ``install`` command
    to set these right away: ``install -m 755 $FIXTURES/<fixture> $STUDENT``.

.. note::
    By default, scripts ran with the ``become_nobody`` command cannot write
    new files to the ``$STUDENT`` directory. Setting the write permission on
    the entire ``$STUDENT`` directory may be undesirable, as students may be
    able to overwrite their own code during the tests. Therefore, we recommend
    you create a new subdirectory where the output should be written with
    ``install -Dm 777 $STUDENT/<SUBDIR>``. If this subdirectory contains files
    that should not be read by students, use permission ``733``.

Global setup script
---------------------

A setup script can be specified which runs prior to the tests to customize the
initial environment. Any script can be uploaded as fixture and subsequently
run with the command given in the *Global setup script to run* input field.

This can be, for example, a bash script that installs software using apt and
extracts archives, or compiles unit tests.

If you need to setup or compile software for each student specifically and not
globally, use the *Per student setup script* for this. Install any packages
using the *Global setup script* as this will greatly increase the speed of
AutoTest Runs

.. warning::
    Setup scripts and other scrips (fixtures) that are executed have to use
    **Unix Line Endings (LF)** and **not** Windows Line Endings (CRLF)!

.. note::
    **Network access** and **Superuser rights** are available during the Setup
    Phase.

Per student setup script
---------------------------

Use the per student setup script to compile, for example, each submission's code.

.. note::
    If you want compiling to be part of a test, use the *Run program* test for
    this.

.. _autotest-automatically-generated-output:

Automatically generated output
------------------------------

It may be desirable have files generated automatically after students submit
their work. This is also possible on the AutoTest infrastructure. While most
generated files (think compilation artifacts) are deleted when the test has
finished, files written to the ``$AT_OUTPUT`` directory are sent back to
CodeGrade so the student and/or teacher can review them later on.

This directory is cleared between each AutoTest category. The generated files
can be viewed in the Code Viewer in the "AutoTest output" category in the file
tree.

.. note::
    By default the ``$AT_OUTPUT`` directory is writable by the user running the
    AutoTest steps. This means that students will also be able to write to this
    directory, or even overwrite files that were generated earlier. To prevent
    this from happening, see also the notes in :ref:`Limiting student access
    <autotest-limit-student-access>`
