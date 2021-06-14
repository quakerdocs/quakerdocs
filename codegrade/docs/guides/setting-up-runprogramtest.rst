Setting up Run Program Tests
================================

.. deprecation_note:: /for-teachers/creating-automatic-tests/creating-run-program-tests

The Run Program Test simply executes a specified program and checks the return
code or exit status of this program. Meaning, an exit status of 0 (or
**success**) results in passing the test and any nonzero exit status (or
**failure**) results in failing the test.

Run Program Tests are easy to set up and effective to check program execution
when specific output is not important. Use Run Program Tests, for instance, to
check the successful compilation of student code or to run single unit tests
that you provide as fixtures.

1. Press the ":fa:`plus` **Run Program**" button to add a new Run Program test to your Test Category.

2. Give the newly added Run Program test a **name**.

    .. note::
        A test's name is the first moment of feedback to the student, more
        extensive and clear names provide better feedback to students.

3. **Optionally**, give the test a **weight**, this defaults to ``1``.

4. Finally, give the command of the **program to test**. The binary exit status (success or fail) of this command will determine the score of the test.

    .. note::
        This program can be handed in or uploaded as fixture, access fixtures in the ``$FIXTURES`` directory.

5. After setting up your IO tests and other tests in your category, press the **Save** button to save.
