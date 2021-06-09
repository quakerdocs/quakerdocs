Student Experience
========================

.. deprecation_note:: /for-students/getting-started

AutoTest is a feedback oriented automatic assessment tool. It makes sure
that students will still receive insightful feedback. To do this, all test
are grouped in test categories that are strongly linked to a rubric category,
so that the tests fill in the rubric category. Together with the possibility to
add extensive naming to individual tests, this allows the student to get
insightful automatic feedback.

.. note::
    It is good practice to be extensive in the naming of the tests. This way,
    students can more easily find out where they have to improve and how.

After an AutoTest has been run, students will find the results of this test
on the submission page of their assignment. This page is easily found via the
LMS.

Continuous Feedback
---------------------
If Continuous Feedback is turned on, students will get near instant automated
feedback for every submission in CodeGrade. Instead of navigating to the
uploaded code after handing in, students will now directly go to the AutoTest
results page with preliminary results.

Visibility of attributes
--------------------------
We believe students should be able to see as much information about the AutoTest
as possible. Sometimes it is however preferred to hide certain test attributes
from students, for instance to re-use tests for the same students at a later
moment.

Students are able to see the following test attributes:

- Test Names
- Test Weights
- Test State
- Points gotten + filling of rubric
- *Executed Command (Program to test and Input Arguments)*
- *Test input and output*
- *Fixtures*

The visibility of the last three items is configurable. Toggle the visibility of
these attributes for an individual test using the :fa:`eye` icon next to this
test. It is also possible to hide the *Executed Command* from students by
removing the permission "View the details of AutoTest steps".

.. note::
    Showing all test attributes to students is recommended for feedback
    purposes.

Automatically generated output
------------------------------

By default, automatically generated output is not visible to students until the
assignment state is set to "Done". This behavior can be changed with the "View
AutoTest output files before done" permission.
