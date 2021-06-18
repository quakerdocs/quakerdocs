.. _guide_use-codegrade-filesystem:

Use the CodeGrade Filesystem to locally mount CodeGrade
========================================================

.. deprecation_note:: /for-teachers/grading-in-codegrade/using-the-filesystem

The CodeGrade Filesystem is a unique way to mount your CodeGrade instance
locally on your system. This provides the teacher much flexibility by allowing
to test, review and grade work from students locally, in your favourite editor
and using all required tools.

The CodeGrade Filesystem is an external application that has to be installed
on your system manually. Please consult the :ref:`installing guide
<guide_install-filesystem>` for instructions on installing the CodeGrade
Filesystem on your operating system.

1. Open the CodeGrade Filesystem application.

2. Select your institution, or select *Other* to enter a custom CodeGrade URL.

3. Enter your username and password.

.. note:: This is your CodeGrade username and password for the selected CodeGrade instance. Click :ref:`here <guide_set-up-password>` to learn how to set up your CodeGrade password.

4. Optionally set advanced options in the *Advanced* tab:

    - **Mount location**: Specify a custom location for the CodeGrade mount, this defaults to the desktop.
    - **Option - Revision mode**: Enable revision mode to save and send all additions, edits and deletions in student submissions back to the student as a *Teacher Revision*. Disable to not synchronise additions, edits or deletions with the CodeGrade server.
    - **Option - Assigned to me**: Enable to only show submissions that are assigned to you. This option only has effect if submissions are actually assigned and you are one of the assignees.
    - **Option - Latest submissions only**: Enable to only show the most recent submission of each student, rather than all their submissions.
    - **Notifications**: Set the verbosity of notifications, default and recommended is *All*.

5. Press *Mount* to mount the CodeGrade server to your computer.

6. Press the pink *mountpoint* on the top of the CodeGrade Filesystem to navigate to the mount. In this directory an organised overview of courses, assignments and submissions can be found, tested and reviewed.

With the CodeGrade Filesystem mounted, you have access to all submissions in
your courses on CodeGrade. These submissions can be opened in your favourite
editor to test, review and grade without any overhead.

Multiple *"special files"* can be found in student submissions too, these are
generated automatically by CodeGrade Filesystem and can be used to review and
grade code. Use the ``.cg_grade`` file to grade work, use the ``.cg_rubric``
file to fill in the rubric (if present) and use the ``.cg_feedback`` file to
write general feedback. Saving these files results in automatically updating
the values on the CodeGrade server too.

.. note:: In addition to our AutoTest platform, the use of the *special files* can allow you to locally run automatic grading scripts that write to the special files to synchronise with the CodeGrade server.

Ultimately, to remove the CodeGrade mount, simply press the *Stop* button or
close the CodeGrade Filesystem application.
