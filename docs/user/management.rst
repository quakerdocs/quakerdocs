.. _management-chapter:

Course and Assignment Management
========================================
The :fa:`cog` button next to courses or assignments is visible to all users with the right
permissions to manage courses or assignments. Clicking this button shows the corresponding
management page.

Additionally, clicking on the name of a course results in an overview of its assignments and
still allows to click the :fa:`cog` button on the bottom right to show the management page.

.. _course-management:

Course Management
-------------------

.. deprecation_note:: /user-reference/courses-general

On the first tab of the course management page, *General*, you can change the
name of the course. The name may not be empty. As the name of LTI courses is
copied from the LMS, the name of LTI courses cannot be changed within
CodeGrade.

On this tab you can also archive a course. Archiving a course will hide it for
students (or more precisely all users that do not have the "See archived
courses" permission), and will sort it below all non archived courses.  You can
still import data from archived courses. Archiving can be reversed without data
loss.

The second tab of the course management page, *Members*, displays a list of all
users (students, teachers and other roles) that are *enrolled* in the
course. The role of users can be changed here and new users can be added to the
course.

.. note::

    Course management is done in your learning management system if the course
    is connected, however managing roles and permissions is still done in
    CodeGrade.

The third tab, *Permissions*, shows an overview of all roles and their specific
permissions. Existing roles can be altered and completely new roles can be added
via the dialog on the bottom of the page. More information about the specific
course permissions can be found in the
:ref:`permissions chapter <permissions-chapter>`.

The fourth tab, *Groups*, shows all group sets of the course. Here you create,
delete and can edit the minimum and maximum size of group sets. Group sets are a
key concept for group assignments in CodeGrade, more information about them can
be found in the :ref:`groups chapter <groups-chapter>`.

The fifth tab, *Snippets*, shows all course-wide snippets in this course. These
course snippets can be set up by the teacher and can be used by all graders
grading in the course. These snippets are always in addition to the graders'
personal snippets and are indicated with the :fa:`books` icon.

Course registration links
~~~~~~~~~~~~~~~~~~~~~~~~~~~

With a course registration link, you can let users sign up to your course via
a URL.

Create a new link under the "Members" tab on the "Course Management" page.
Then set both "Expiration date" and "Role" and save your link. The link will
become invalid once the expiration date has passed or when the link is deleted.
When a link is invalid, it is no longer possible to register for the course with
that link.

"Role" is the role that is assigned to the users that register via the link.
You can have multiple links with different roles, e.g. one for students to
sign up and one for teachers or TAs to sign up.

.. warning::
    You don't want to add a course registration link to LTI courses
    (courses that are connected to your Learning Management System), as all
    course registration should come from the LMS.

.. note::
    *Everyone* with access to this link will be able to register for your course.
    Currently, it's not possible to delete users from a course, so be careful
    when sharing the link. Contact us if you wish to delete users.

Creating a new Course
~~~~~~~~~~~~~~~~~~~~~~
Specific :ref:`site permissions <site-permissions>` are required to create a
course, usually this can be done only be site administrators. If these
permissions are set, a course can be created by navigating to the courses menu
and clicking the :fa:`plus` icon. The name for the new course can then be given.

.. _assignment-management:

Assignment Management
----------------------

.. deprecation_note:: /user-reference/assignments

Clicking the :fa:`cog` button next to a specific assignment shows the assignment
management page. Usually all teachers and course designers can manage
courses and assignments.

.. _manage-assignment-state:

Assignment State
~~~~~~~~~~~~~~~~~~~
Three assignment states are available and can be set on the top right:

- :fa:`eye-slash` **Hidden** state: the assignment is invisible to students.
- :fa:`clock-o` **Open** state: the assignment is visible to students and
  students can hand in submissions before the deadline.
- :fa:`check` **Done** state: the assignment is visible to students and grading
  is finished.

General
~~~~~~~~
In this tab you can edit basic settings, such as the assignment name and
deadline, but also some more advanced settings.

Assignment type
+++++++++++++++
A CodeGrade assignment can be one of three types:

- **Normal**: a regular assignment.
- **Exam**: an exam. For exams you do not configure the deadline of an
  assignment but rather when it starts and a duration. Students can optionally
  receive an email with a link with which they can set a password and log into
  CodeGrade when the exam starts. During the exam students only have access to
  the course of the exam, and not any other courses.

  See the :ref:`Exam mode documentation <exam-mode>` documentation for more
  information about exams in CodeGrade.
- **LTI**: an assignment managed via a Learning Management System. You cannot
  switch to one of the other types of assignment.

Available at
++++++++++++
The available at date of an assignment automates the transition from the
**hidden** state of the assignment to the **open** state. Set a date and time
and at that moment the assignment will become visible to students, so you don't
have to think about it anymore.

Upload types
+++++++++++++
CodeGrade offers two means of handing in for students: via the file uploader
in CodeGrade or using Git (GitHub or GitLab).

- **File Uploader**: this option allows students to hand in their submission
  through CodeGrade's file uploader. Students can hand in one or multiple files
  and can even hand in archives (e.g. ``.zip`` or ``.tar.gz``) which will be
  extracted automatically.
- **Git**: this option allows students to configure their GitHub or GitLab
  repository to upload to CodeGrade with every ``push``. Configuration
  instructions can be found on the hand-in page, the unique deploy key and
  webhook have to be configured for each separate assignment once per student.

.. note::

    It is possible to use both the File Uploader and Git upload type together for the same assignment. Students can then choose which means of handing in they prefer.

Git uploading
##############
CodeGrade allows students to hand in directly via GitHub or GitLab if the
**Git upload type** is turned on for an assignment. Students can find
instructions to configure their repository on the hand in page.

Setting up your repository to work together with CodeGrade is done with a
*deploy key* and *webhook*. The deploy key is used to grant CodeGrade access
to read your repository. The webhook is used to notify CodeGrade for each push
event that takes place. With this setup, students will automatically upload
their work to CodeGrade every time they ``push``.

.. warning::

    CodeGrade has a size limit on student submissions. Exceeding this size limit
    will result in a warning message when regularly handing in, but not when
    using git to upload. If a student exceeds this limit, files exceeding the
    limit are silently deleted. This very rare case does result in a
    ``cg-size-limit-exceeded`` file to show up in the Code Viewer.

Uploading via Git works together with CodeGrade's tools, use it in
combination with Continuous Feedback and AutoTest to provide immediate and
automatic feedback to students every time they submit. It is also possible to
combine Git uploading with group assignments. All students in a group will share
the deploy key and webhook, anyone in the group can hand in for the whole group
with a ``git push``. Just like with regular handing in, all group members will
have to open the CodeGrade assignment in their LMS (Canvas, Blackboard,
Brightspace or Moodle).

.. warning::

    Hand-In Requirements are **disabled** when using the Git upload type.

In addition to further streamlining the workflow for students, Git uploading
allows teachers to also assess git usage within CodeGrade. This can be done
manually, by looking at the ``.git`` folder in the Code Viewer or directly
opening the student repository by clicking the GitLab or GitHub link in the
submission. In AutoTest, the student submission is a normal Git
directory and can be handled and assessed that way automatically.

.. note::

    Using git in AutoTest? Run ``git fetch --unshallow`` to make sure the
    information in the ``.git`` folder is complete and shows all history.

More information on setting up Git uploading can be found in the
:ref:`step-by-step guide <guide_git_uploads>`.

Limiting the amount of submissions
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

By setting the maximum amount of submissions, and the *cool off period* you can
limit the number of times students can hand-in.

Maximum submissions
###################

By setting the maximum amount of submissions you can limit how many submissions
a student can make in total for an assignment. If you set this to value to
anything higher than 0 this is the total amount of submissions the student can
make. They will be informed of this limit when they create a new submission. You
can disable this limit by setting the limit to "0" or "infinite".

Cool off period
####################

The cool off period allows for a more advanced way of limiting the amount of
submissions a student can create. Instead of setting a limit for the entire
assignment, you can set a limit for a certain time frame in an assignment. This
allows you to effectively set an amount of submissions a student may create in a
certain time period.

.. example::

    When the cool off period is set to "2 submissions every 10 minutes", and a
    student submits at 10:00, and at 10:05 it will be impossible for this
    student to submit again before 10:10. If the student submits again at 10:11,
    it will now be impossible to submit again before 10:15.

You can combine the *cool off period* with a maximum amount of submissions. This
could allow you, for example, to enforce a small wait period between two
submissions, but also enforce a total amount of submissions.

Uploading Submissions
+++++++++++++++++++++++
Submissions can be uploaded via the assignment management page too. Using the
*Upload submission* tool submissions can be uploaded as any requested user:
hand in submissions for students or hand in as administrator by selecting
a user via the search bar. Submissions can be uploaded as an archive, which is
automatically extracted by CodeGrade, or as multiple individual files.

You can also do a submission as a test student to check if your assignment
setup works as expected. It can be useful to test your hand-in requirements,
AutoTest configuration, you name it. You can even do test submissions before
you have set a deadline on the assignment.

Peer feedback
+++++++++++++
Who knows better what problems students run into than the students themselves?
This is why CodeGrade offers peer feedback, a way for students to review and
learn from each other's code. When peer feedback is enabled for an assignment
students get assigned to a number of other students and get access to their
submissions.

You can enable peer feedback by clicking the :fa:`comments-o` button,
configuring the peer feedback settings, and finally pressing the "Submit"
button.

Amount of students
##################
This is the amount of submissions each student should review. Students are
distributed randomly amongst each other. This happens in an auomated fashion
once the deadline of the assignment has passed.

.. warning::

   This setting should be treated with care, *especially after the assignment's
   deadline*, because changing it will cause all students to be reassigned. The
   process of reassigning does not guarantee that students are assigned to the
   same peers as before the change, even when the number has increased. On the
   contrary, it is quite likely that almost all students are assigned to
   someone else than they had been.

Time to give peer feedback
##########################
The amount of time students have to give feedback to their peers. During this
time students can place comments on the submissions they were assigned to.
Students will still be able to view the submissions even after this time has
passed.

Automatically approve comments
##############################
By default when a student places peer feedback on another student's submission
the other student will not be able to see it immediately. The comment first has
to be approved by the teacher or teaching assistant. Enabling this option
changes that behavior so that each comment is automatically approved.

.. note::

  Comments can still be disapproved even with this setting turned on.

Group assignment
++++++++++++++++++
Here you can select which group set to use for this assignment. When a group set
is selected the assignment becomes a group assignment. Group sets are a
key concept for group assignments in CodeGrade, more information about them can
be found in the :ref:`groups chapter <groups-chapter>`.

Hand-in Requirements
++++++++++++++++++++++
The hand-in requirements make it possible to set up strict rules to the
structure requested for submissions to a specific assignment. Hand-in
requirements consist of three different parts that specify the behaviour of
your requirements.

First, a default policy should be selected: **by default deny all files** or
**by default allow all files**. Exceptions to these rules can be given in the
third part of the specifications.

Secondly, numerous options can be selected to further specify the behaviour of
your requirements. These options are:

- **Delete empty directories**: If enabled, automatically delete empty
  directories in submissions.
- **Delete leading directories**: If enabled, automatically delete superfluous
  leading directories (i.e. top-level directories in which all files
  / subdirectories are located).
- **Allow overrides by students**: If enabled, the student can, after being
  shown a warning, still force hand in the submission even if it violates the
  hand-in requirements.

Thirdly, rules can be given that consist of exceptions to the default rule and
requiring certain files. These rules can apply to files anywhere in the
submission or files that have to be in an given path relative to the top level
directory. These rules are individual and do not have any ordering between them.

.. note::

    Use ``/`` or ``\`` as a directory separator to specify that certain files are
    required, allowed or denied in a directory. Start the rule with a directory
    separator (``/`` or ``\``) to specify that a file is required, allowed or denied in
    the top level directory.

    To match more than one file, you can use a single wildcard for the name of
    the file, by using a ``*``. For example ``/src/*.py`` matches any file ending with
    ``.py`` in the directory src that is directly in the top level directory of the
    submission.

More information on setting up hand-in requirements can be found in the
:ref:`step-by-step guide <guide_hand_in_requirements>`.

Group assignment
++++++++++++++++++
Here you can select which group set to use for this assignment. When a group set
is selected the assignment becomes a group assignment. Group sets are a
key concept for group assignments in CodeGrade, more information about them can
be found in the :ref:`groups chapter <groups-chapter>`.

.. _upload-blackboard-zip:

Graders
~~~~~~~~~
In this tab you can edit all settings regarding graders, like dividing and
setting up notifications for them.

Dividing Submissions
+++++++++++++++++++++
To randomly and automatically assign graders to all submissions the Divide
Submission feature on the assignment management page can be used. A list of all
graders is displayed and after selecting the wanted graders weights can be given
to affect the workload per grader. The resulting percentage is the percentage of
submissions the grader will be randomly assigned to. Newly submitted submissions
are automatically assigned to graders after dividing is performed.  Dividing
submissions is consistent, so new submissions will get assigned to the same
teaching assistant.

Manually assigning submissions is possible via the submission list, by selecting
the grader using the 'Assigned to' dropdown dialog.

It is also possible to link the divisions and assignees of multiple
assignments. To do this you can select a parent assignment in the selector below
the weights of the graders. When an assignment is connected to another
assignment, the child assignment copies the settings and assignees of the parent
assignment. After linking, the division settings of the parent and the child are
frozen. Multiple assignments can be linked to the same parent, however a parent
cannot be linked to another assignment as a child.

When a student submits to a child or parent assignment CodeGrade tries to assign
the student to the same assignee as in other assignments. It does this by first
copying the assignee of the parent assignment for the submitting student, or if
this is not possible selecting the most common assignee in the children
assignments.

.. note::

    When teachers manually assign themselves, weights are not updated to reflect
    this.

Finished Grading and Notifications
+++++++++++++++++++++++++++++++++++
CodeGrade provides essential communication tools between graders in the shape of
email notifications. These notifications rely on graders indicating that they
are done grading by setting their state to 'Done' after all grading is finished.

.. warning::

    It is possible to set a grader to the 'Done' state that did not finish
    grading all assigned submissions, a warning is shown in this case.

E-mail Notifications
++++++++++++++++++++++
CodeGrade provides two types of email notifications to enable essential
communication between graders:

* **Graders** notification: send an email at a specified date and time to all
  graders that have not yet finished grading.
* **Finished** notification: send an email to a specified email address to
  notify when all graders are finished grading.

.. note:: For these notifications to be sent, graders must manually update
   their status.

Plagiarism
~~~~~~~~~~~~~~~~~~~~~~
CodeGrade offers built in plagiarism detection functionalities, to efficiently
and clearly detect for plagiarism on programming assignments. In this tab you
can configure plagiarism runs. Please consult the :ref:`Plagiarism Detection
<plagiarism-chapter>` chapter for more information.

Rubric
~~~~~~~~~~
Rubrics are an indispensable tool in modern day education and allow for easy and
consistent grading between different graders and submissions. In this tab you
can setup and edit the rubric of the assignment. Sophisticated rubrics can be
made in CodeGrade. A basic rubric consist of multiple categories that all have
multiple levels and corresponding points. All components in a CodeGrade rubric
can have a name and description.

A new rubric can be created by clicking the :fa:`plus` button. You can also
import a rubric by clicking the :fa:`copy` button.

After creating a new rubric or copying an existing rubric you can add
categories by pressing :fa:`plus` at the end of the list of categories. There
are two types of categories:

Discrete rubric categories
++++++++++++++++++++++++++++

Discrete rubric categories are rubric categories with multiple levels, each
assigned a number of points, in them. When grading one level in a category can
be selected. New levels can be created by clicking on the empty level with the
large :fa:`plus` in it. You can remove levels by pressing the :fa:`times`
button.

Continuous rubric categories
++++++++++++++++++++++++++++

Besides the more traditional discrete categories, CodeGrade also offers
continuous categories. Continuous categories are assigned a maximum amount of
points (which should be higher than 0), and when grading any amount of points
between 0 and the set maximum can be assigned for the category. This allows you,
for example, to split your grade into multiple categories, while still allowing
precise grading. Continuous rubric categories are also very useful for
:ref:`AutoTest <autotest-overview>`.

.. tip::

    A rubric is only saved after pressing the 'Submit' button, it is recommended
    to occasionally save the rubric to prevent losing work.

AutoTest
~~~~~~~~~
The AutoTest configuration and results can be viewed and edited in the AutoTest
tab. For more information on how to set up AutoTest refer to
:ref:`the AutoTest documentation <autotest-overview>`.

Creating a new Assignment
~~~~~~~~~~~~~~~~~~~~~~~~~
With the right :ref:`permissions <permissions-chapter>` new assignments for a
course can be created. To do this, select the course in the Course menu and
click on it to display its assignment list. A new assignment can now be created
for this course using the :fa:`plus` button on the bottom of the
menu-screen. Press *Add* after specifying a name for the assignment to create
it.
