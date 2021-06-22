.. _set-up-group-assignment:

Set up a CodeGrade group assignment
======================================================

.. deprecation_note:: /for-teachers/configuring-your-assignment/making-a-group-assignment

Groups for group assignments are managed entirely within CodeGrade. Group sets
are created in CodeGrade on a course-level, meaning that multiple assignments
within one course can have the same groups.

.. warning::

    It is important that a regular individual assignment is created within your LMS (
    Canvas, Blackboard, Moodle or BrightSpace), and **not** a group assignment.
    CodeGrade handles all the groups and makes sure grades and feedback is
    passed back correctly to the corresponding group members. Click
    :ref:`here <creating_assignment_guide>` to find out how to create a
    CodeGrade assignment.

1. A group set for your course in CodeGrade has to be created firstly. Click the :fa:`cog` button next to your course to go to the **"Course Management"** page.

2. Navigate to the **"Groups"** tab to find an overview of previously created group sets or to create a new group set.

3. Click the **"Add group set"** button to create a new group set, specify the minimum and maximum group sizes and press :fa:`save` to save.

    .. note::

        If minimum group size is set to **1**, individual users that are not in
        a group can still hand in submissions too.

4. Now that a new group set is created, this group set can be linked to assignments. Go to the **"Assignment Management"** page of the assignment you want to make a group assignment by clicking the :fa:`cog` button.

5. On the **"General"** tab, scroll down to the **"Group Assignment"** section. Here, select the desired group set and confirm by pressing **"Submit"**. Your assignment is now a group assignment!

By default, students can create new groups and join groups within a group set
themselves. The names of groups are automatically generated but can be manually
changed afterwards. If you want to change this default behaviour (e.g. make it
impossible for students to create or join groups themselves), please consult the
:ref:`permissions documentation <permissions-chapter>` to find out more about
the permissions that make this possible.
