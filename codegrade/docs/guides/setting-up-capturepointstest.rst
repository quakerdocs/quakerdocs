Setting up Capture Points Tests
================================

.. deprecation_note:: /for-teachers/creating-automatic-tests/creating-capture-points-tests

With a Capture Points test you can easily run and integrate your own unit
test scripts. A Capture Points Test captures the output of the executed program
with a Python3 Regular Expression. This output should be a **number between
0 and 1**.

1. Press the ":fa:`plus` **Capture Points**" button to add a new Capture Points
   test to your Test Category.

2. Input which program you want to execute.

3. Specify the **Python3 Regex** with which you want to capture the output. By
   default this captures a single float. This number is multiplied by the
   **weight** to get the amount of points.

   .. note::

       A **Python3 Regex** may contain ``\f``, which will capture a float.

.. note::
    We recommend you run your program with our utility program
    ``normalize_floats`` to ensure that the score you write can be read
    correctly by CodeGrade. For example, if the command to run your tests is
    ``run_tests``, you would run ``normalize_floats 2 run_tests`` to output the
    score with 2 decimals precision.

.. note::
    While linters and unit testing frameworks can be run in a "Capture Points"
    step, more advanced solutions for those specific tasks are available.
    Linters can be run using the :ref:`Code Quality <setting-up-code-quality>`
    step, and unit testing frameworks with the :ref:`Unit Test
    <setting-up-unit-tests>` step.
