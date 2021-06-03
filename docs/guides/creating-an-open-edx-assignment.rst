Create a CodeGrade assignment in Open edX
================================================

.. deprecation_note:: /for-teachers/creating-an-assignment/in-open-edx

.. note::

    The guide below assumes CodeGrade has been successfully integrated into
    your Open edX environment as external LTI app.

Creating a new CodeGrade assignment from within Open edX will correctly
add this assignment to the corresponding course in CodeGrade, a new course will
automatically be created in CodeGrade if it does not yet exist in CodeGrade.
Follow the steps below to create a new CodeGrade assignment in Open edX:

1. Edit the unit in which you want to add CodeGrade and select
   **Advanced** from the **Add New Component** section. Select **LTI Consumer**.

2. Select **Edit** in the component that appears. This should open a modal in
   which you can set up the CodeGrade assignment.

3. Set the **Display Name** to the name of the assignment.

4. The value for **LTI ID** depends on the configuration that your
   administrator set, however this will probably be ``codegrade``.

5. The **LTI URL** is ``https://app.codegra.de/api/v1/lti/launch/1``, however
   for instances with a custom URL this will be different. Please contact us at
   `support@codegrade.com <mailto:support@codegrade.com>`__.

6. Now scroll all the way to the bottom and make sure the following options are
   all set to **True**:

   - Scored, this option allows to passback a grade for the assignment
   - Request user’s email
   - Request user's full name
   - Request user’s username

7. Click the save button.

.. note::

    Grades are automatically sent back to Open edX after setting the
    **assignment state** to (:fa:`check`) **Done** in CodeGrade. While the
    assignment is in the (:fa:`check`) **Done** state, all grades and changes to
    grades are immediately sent back to Open edX.

.. note::
    Students can hand in and review their feedback from within the CodeGrade
    container in Open edX.
