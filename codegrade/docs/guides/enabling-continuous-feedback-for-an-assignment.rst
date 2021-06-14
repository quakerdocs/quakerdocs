Enabling Continuous Feedback for an assignment
================================================================

.. deprecation_note:: /for-teachers/creating-automatic-tests/giving-students-instant-feedback

CodeGrade Continuous Feedback allows students to instantly get insightful
automated feedback every time they hand in a new revision of their submission.
The tests that run in Continuous Feedback are (a subset of) the AutoTest tests,
this means that Continuous Feedback has the same security and reliability as
CodeGrade AutoTest.

To enable Continuous Feedback for a CodeGrade assignment, first make sure an
AutoTest is set up. Please follow the steps in
:ref:`Setting up AutoTest <setting-up-autotest>` to learn how to do this. After
your desired tests are set up, follow the steps below to enable Continuous
Feedback:

1. Go to the **Assignment Management** page by clicking on the :fa:`cog` icon.

2. Navigate to the **AutoTest** page.

3. Set up the AutoTest for your assignment by following the steps in the :ref:`Setting up AutoTest guide<setting-up-autotest>`.

4. All created AutoTest tests are automatically used for Continuous Feedback too. Differentiate between AutoTest and Continuous Feedback by hiding and disabling individual tests for Continuous Feedback, this is done by pressing the :fa:`eye` button next to the test.

5. After setting up AutoTest and hiding and disabling individual tests you do not want used in Continuous Feedback, turn on Continuous Feedback for your assignment by setting the *Results Visibility* mode to *Immediate*.

Continuous Feedback is now turned on for your assignment. Near instant feedback
will be presented to the students for every submission they make.

.. warning::
    If you have created hidden steps, the rubric is not filled in immediately,
    but only after the deadline of the assignment has passed.
