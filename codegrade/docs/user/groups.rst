.. _groups-chapter:

Groups
========

.. deprecation_note:: /user-reference/groups

CodeGrade supports group assignments through the concept of *group sets* and
*groups*. This chapter explains these concepts and how to create and use group
assignments.

Group set
-----------
Groups are connected to a *group set*, this group set is in turn is coupled to
zero or more assignments. A group set determines the minimum and maximum size
for each group in this group set. To create a group set go to the
:ref:`course management page <course-management>` and select the *Groups*
tab. Here you can add and delete group sets.

After you have created a group set you can connect this group set to an
assignment. To do this go to the
:ref:`assignment management page <assignment-management>` and go to the *Group
Assignment* tab, select the wanted group set and press *Submit*. You can connect
a group set to multiple assignments, which then share the same groups.

When an assignment is a group assignment it is impossible for students to submit
when they are not in a group, or when their group is smaller than the minimum
size.

Groups
--------
Groups are connected to a group set. For each group set students are connected
to one or zero groups.

When navigating pages of a course with group sets a new button should appear in
the sidebar, the *Groups* button. After clicking on this button and selecting a
group set you can add, delete and change groups for this group set. By default
students can join groups, leave groups, and edit the name of their group. See
:ref:`permissions chapter <permissions-chapter>` for more information. Students
also get prompted a pop-up when submitting to a group assignment if they are not
in a group or if their group is too small. Using they pop-up they can join and
create groups. It is currently not possible to randomly assign students to
groups.
