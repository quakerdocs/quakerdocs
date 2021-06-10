How to use CodeGrade as a student
================================================

.. deprecation_note:: /for-students/getting-started

Using CodeGrade as a student is easy and offers you the ability to get a lot
more feedback and optionally automated test results.

When you open an assignment in CodeGrade or your LMS (Blackboard, Brightspace,
Canvas, Moddle, etc.) you are presented with a number of actions you can
perform.

- **Latest submission**: Go to your latest submission.

- **Upload files**: Create a new submission by uploading files.

- **Set up Git**: Show instructions on how to connect a Git provider to your
  assignment, this allows you to create submissions by pushing to a Git
  repository.

- **Rubric**: Show the rubric of this assignment.

- **Groups**: Create and/or join groups.

- **Peer feedback**: Give feedback to your fellow students.

- **Course feedback**: Show an overview of the feedback you received to all
  assignments of this course.

.. note::
    Some of these are not available when they are not applicable, e.g. when an
    assignment is not set up as a group assignment, the groups button will be
    hidden.

Handing in
-----------

1. Click the "Upload files" button.

2. Optionally, if the teacher has set hand-in instructions, they are displayed
   at the top of the page. Make sure to follow your teacher's requirements when
   uploading files!

3. You can either drag and drop files onto the upload field or select them via
   your browser’s file picker dialog. You can either upload separate files, or
   an archive (such as a zip or tar). Archives are automatically extracted (but
   archives contained in other archives are not).

4. Press submit.

5. If the teacher enabled Continuous Feedback, you will now be able to see
   Automated Test results coming in (this might take a few minutes).

.. note::

    Keep in mind that Continuous Feedback is preliminary, and the rubric will
    not yet be filled in. You only get a grade after the deadline when the
    teacher graded your assignment.

6. Click on tests to see why they succeeded or failed. Improve your code and
   try again.

.. note::

    Always test your code first on your own system to make sure it works,
    before uploading to CodeGrade.

Handing in with Git
~~~~~~~~~~~~~~~~~~~~~

Some CodeGrade assignments allow you to hand in code by pushing to a Git
repository (GitLab or Github). If an assignment is set up to allow for Git
submissions the "Set up Git" button shows you instructions on how to set up a
deploy key and webhook URL for your repository.

.. note::

    Working in a group **and** handing in using Git? Make sure all members of
    the group have opened the CodeGrade assignment in Canvas, Moodle,
    Blackboard or Brightspace before handing in. *This does not apply to stand-
    alone usage of CodeGrade!*

.. warning::

    CodeGrade has a size limit for uploading submissions. Handing in via git
    can result in files exceeding this size limit to be silently deleted. Always
    check your submission in CodeGrade when working with large repositories.
    *If the size limit is exceeded, a file named ``cg-size-limit-exceeded``
    will show up in your submission.*

Viewing feedback
-----------------

After your assignment is graded, you can view your feedback through CodeGrade.

1. Navigate to the assignment, or click on your grade in the grade center.

2. View your feedback. On the Feedback Overview, you can view your inline
   feedback comments with some context. Browse to the Code to view the inline
   feedback with all of your code. Finally, on the AutoTest tab you can view
   the output of the Automated Testing system.

Giving peer feedback
---------------------

When an assignment is set up as a peer feedback assignment, you can review
assignments of your fellow students by clicking on the "Peer feedback" button.
You are now presented with a list of the other students you have to review. At
the bottom of the list it tells you the deadline for giving peer feedback.

After you click on the student you want to review, you are taken to the Code
Viewer page of their latest submission. Click on any line of code to comment on
it.

.. note::

    It may be possible that the other student does not receive your feedback
    immediately. This happens when your teacher has set up the assignment to
    not automatically approve peer feedback comments. In this case a teacher or
    teaching assistant must manually approve a comment for it to be published
    to the other student.

Number of given comments
~~~~~~~~~~~~~~~~~~~~~~~~

On the right side of the list with students you have to review, it shows the
number of comments you have already given to each student. It may contain two
numbers when the other student has done another submission after you have
already given them some feedback. If this happens, the first number is the
amount of comments you have given on their latest submission, and the
second is the total amount of comments you placed on all of their submissions
(the last one included).

Viewing peer feedback
---------------------

On the Code Viewer page of your own submission, the feedback you have received
will be visible within your code, just like the feedback you receive from your
teacher. You can also go to the feedback overview to get an overview of all
feedback you have received, both from teachers and your peers.

An extra "Peer Feedback" tab is also available on the Code Viewer page, where
you can get an overview of all feedback you have given. Click on the entries on
the right side of the page to move between students and files. At the bottom of
this page it shows you a list of students you have been assigned but have not
yet given feedback to, if any.
