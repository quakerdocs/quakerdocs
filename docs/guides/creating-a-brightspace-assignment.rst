Create a CodeGrade assignment in BrightSpace
=====================================================

.. deprecation_note:: /for-teachers/creating-an-assignment/in-brightspace

.. note::

    The guide below assumes CodeGrade has been successfully integrated into
    your BrightSpace environment as external LTI app.

Creating a new CodeGrade assignment in BrightSpace will correctly
add this assignment to the corresponding course in CodeGrade, a new course will
automatically be created in CodeGrade if it doesn't exist. Follow
the steps below to create a new CodeGrade assignment in BrightSpace:

1. Navigate to the homepage of the course to create the assignment in.

2. Click the **"Content"** button at the top of the page.

3. In the **"Add Existing Activities"** dropdown, click **"External Learning Tools"** to open a new dialog.

4. Click the **"Create new LTI Link"** at the bottom of the dialog *(you may need to scroll)*.

5. Enter the assignment's name in the **"Title"** field.

6. Enter the CodeGrade url, e.g. ``https://<your-institution>.codegra.de/api/v1/lti/launch/1``.

.. note::

    The LTI Tool will be automatically selected after filling in the above URL as *Legacy LTI Tool*.

7. Click **"Create and Insert"** to create your CodeGrade assignment in BrightSpace.


.. warning::

    Never set a **Due Date** in BrightSpace, instead manage the due date inside CodeGrade.

.. note::

    Grades are automatically sent back to BrightSpace after setting the
    **assignment state** to (:fa:`check`) **Done** in CodeGrade. While the
    assignment is in the (:fa:`check`) **Done** state, all grades and changes to
    grades are immediately sent back to BrightSpace.

.. note::
    Students can hand in and review their feedback from within the CodeGrade
    container in BrightSpace.
