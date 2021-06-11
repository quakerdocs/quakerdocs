.. _setting-up-code-quality:

Setting up Code Quality tests
==============================

.. deprecation_note:: /for-teachers/creating-automatic-tests/creating-code-quality-tests

The Code Quality test runs a linter or other program that produces feedback
on the code, which is stored and displayed inline in the student's code.

The resulting score of this test is determined by the amount of comments that
were produced by the linter. Each comment has a severity, which is determined
by the linter, and for each different severity level you can configure an
amount of points to be subtracted from the score.

There are four severity levels: **fatal**, **error**, **warning**, and
**info**.

The final score is the score left over from subtracting the penalty of each
comment from the initial score of 100, interpreted as a percentage, multiplied
by the weight of the step.

1. Press the ":fa:`plus` **Code Quality**" button to add a new Code Quality
   test to your Test Category.

2. Select the linter you want to run from the dropdown menu, or select "custom"
   if you want to run a linter that is not present in the list.

3. If you selected a linter from the list, you can enter a configuration file
   to be used by the linter, and any extra arguments to be passed to the linter
   program. If you chose "custom", enter the program to be ran.

4. Configure the penalties for each severity level, as described above.
