.. _autotest-overview:

AutoTest
================================

.. deprecation_note:: /user-reference/autotest-general

AutoTest is CodeGrade's highly flexible and highly customizable Automatic
Grading Environment. With AutoTest you can fully configure a Virtual Machine
to suit the needs of your assignments. Via the intuitive user interface you can
easily create simple input/output tests or run custom programs or unit tests.

AutoTest provides a lightweight Virtual Machine for each submission within an
assignment running Ubuntu (Linux), this Virtual Machine is fully configurable
and you can install anything you want on this VM. With most popular languages
and tools already pre-installed on every VM. Each assignment runs on a dedicated
Virtual Private Server (VPS) providing a hard division between assignments and
maximum security and privacy. AutoTest is secure by default and by design.

AutoTest Tests are grouped into Categories, each AutoTest Category is then connected
to a Rubric Category. By connecting AutoTest to the rubric, students still get
feedback even when automatically grading. It also forces teachers
to group their tests in a meaningful way.

AutoTest Categories are grouped into Levels. Usually one Level is enough, but there
are some use-cases in which you would want to create multiple Levels.

Running AutoTest is easy and straightforward. After a run the results are visible
to students from within the Code Viewer.

.. toctree::
    :maxdepth: 1

    setup
    levels
    categories
    tests
    continuous-feedback
    running-autotest
    student-experience
