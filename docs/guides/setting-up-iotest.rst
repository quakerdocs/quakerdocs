Setting up IO Tests
================================

.. deprecation_note:: /for-teachers/creating-automatic-tests/creating-input-and-output-tests

The IO Test is the most common test to create. This is a test in which you
specify an input to a program and an expected output. If the students' program
returns the same output as expected, the test passes and they achieve points.

IO Tests are easily created in the CodeGrade AutoTest user interface. One single
IO test can have multiple sets of input and output.

1. Press the ":fa:`plus` **IO Test**" button to add a new IO test to your Test Category.

2. Give the newly added IO Test a **name**.

    .. note::
        A test's name is the first moment of feedback to the student, more
        extensive and clear names provide better feedback to students.

3. Give the command that runs the **program to test**, this can be a program handed in by the student or a program that was installed or uploaded as fixture.

4. Set up one or more input and output combinations, each input and output combination defaults to a weight of one (change this in *Advanced Options*) and has a name. More input output combinations can be added by pressing the ":fa:`plus` **Input**" button:

    a. Again, give the **name** of the specific input and output combination.

    b. Give the input, either as **Input Arguments** or as **Input** via standard input.

    .. note::
        You can use uploaded fixtures as input arguments too, access them in the ``$FIXTURES`` directory.

    c. Give the **expected output**, which can be parsed with the following options:

        - **Case insensitive**: comparing of student output and expected output is case insensitive.
        - **Ignore trailing whitespace**: trailing whitespace is ignored when comparing the student output with the expected output.
        - **Ignore all whitespace**: all whitespace is ignored when comparing the student output with the expected output (including newlines).
        - **Substring**: comparing of student output and expected output is done with substring matching. As long as the expected output is present as a substring in the student output, the test succeeds.
        - **Regex**: the expected output is a *Python3 Regex* which should match with the actual output.

        .. note::
            The options *Ignore all whitespace* and *regex* cannot be activated
            together.

        .. note::
            The option *substring* is required when using the *regex* option.

5. After setting up your IO tests and other tests in your category, press the **Save** button to save.
