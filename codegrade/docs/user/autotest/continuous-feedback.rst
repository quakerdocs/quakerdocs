.. _cont-feedback:

Continuous Feedback
======================

.. deprecation_note:: /for-teachers/creating-automatic-tests/giving-students-instant-feedback

CodeGrade Continuous Feedback allows students to instantly get insightful
automated feedback every time they hand in a new revision of their submission.

The results of Continuous Feedback allow
students to revise their work and start processing feedback even before the
deadline.

Setup
---------
Continuous Feedback uses the AutoTest configuration and tests. Enabling
Continuous Feedback for your assignment can be done by setting the :ref:`Result Visibility <at-result-visibility>`
to Immediate.

Differentiate between AutoTest and Continuous Feedback
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
It is oftentimes wished to not include all tests in your Continuous Feedback
runs. Disable and hide an individual test for Continuous Feedback by toggling
the :fa:`eye` button next to this test. This results in the test not being
executed in the Continuous Feedback runs and hides details from students in the
AutoTest results. AutoTest is automatically run again within 30 minutes after the
deadline to execute the hidden steps.

.. note::
    It is good practice to disable heavy / long tests in the Continuous Feedback
    runs to optimize performance.
