Graders
~~~~~~~~~

To divide submissions between your teachers and/or TAs, graders can be assigned
to individual submissions. This can be done either *manually*, using the dropdown
menus on the submission list page, or *randomly* using the **“Divide Submissions”**
tool on the “Graders” page on the assignment management page.

Submission divisions can be *shared* between different assignments of the same
course. Connect the submission division with another assignment to use the
previously created division.
:ref:`Click here to learn more about dividing submissions <dividing-submissions>`

.. note::
    Connecting divisions can be very helpful if you want the same TAs
    to grade the same students for each assignment.

Plagiarism
~~~~~~~~~~~

On the **"Plagiarism"** page it is possible to start plagiarism runs to detect fraud.
:ref:`Click here to find out more about starting plagiarism runs <checking-for-plagiarism>`

Rubric
~~~~~~~~~

Rubrics are a scoring guide used by graders, they make grading more **consistent**
and **efficient** for teachers, and help students **understand** their grade. Rubrics
can be created within CodeGrade and consist of multiple categories. Each
category has multiple levels, with a corresponding amount of points.
Examples of categories are *functionality*, *code style*, *documentation*,
*code structure* and *version control*. Examples of levels are *unacceptable (0)*,
*needs improvement (1)*, *good (2)* and *excellent (3)*. CodeGrade will **automatically
calculate** the grade after filling in the rubric, by taking the sum of the
points and dividing this by the maximum amount of points.
This grade can be overridden. :ref:`Click here to learn more about setting up rubrics <set-up-rubric>`

.. note::
    Rubrics can also be imported from previous assignments.

The Code Viewer
==================

The heart of CodeGrade is the Code Viewer. This enables you to grade and review
submissions from within our website and allows students to intuitively see
their feedback displayed in their code.

*Submissions* handed in as archives are *automatically* extracted and displayed
in the file-tree next to the *Code Viewer*. Of course, multiple individual files
can also be uploaded in CodeGrade. The Code Viewer supports over **175
programming languages**, **Jupyter Notebooks**, **PDF-files** and **images**.

Inline feedback
~~~~~~~~~~~~~~~~

The most intuitive way to give feedback on programming assignments is to be
able to write comments on **specific lines or blocks of code**. This is made
possible by the **inline feedback** in the Code Viewer.

Press on any line and start
typing your feedback, click the :fa:`check` button to save the feedback or press the
:fa:`cross` button to delete.

.. note::
    Pro tip: press :kbd:`Ctrl+Enter` to save feedback efficiently.

Snippets
~~~~~~~~~

Experience tells us that the same lines of feedback are oftentimes given
multiple times to multiple students. We introduced **snippets** to make grading
with inline feedback **more efficient**. Click the :fa:`plus` icon when entering line
feedback to save the comment as a snippet. This snippet can now be re-used
in the future by **typing its short name** and pressing :kbd:`Tab` to autocomplete.

Full management of snippets can be done in the **“Profile Page"** (:fa:`user-circle-o`),
snippets are personal and can be used over multiple assignments and courses.

.. note::

    Course wide snippets are available in CodeGrade too, these can be set up by
    the teacher of the course on the **Course Management page** and can be used
    by all graders of the course.

Rubrics
~~~~~~~~

If an assignment has a rubric (:ref:`click here to learn more about setting up rubrics <set-up-rubric>`),
the rubric **can be used and filled in** from within the Code Viewer.
Press the :fa:`th` button to display the rubric and select the levels for the
submission to generate a grade using the rubric.

.. warning::
    **Do not forget to save the filled in rubric after grading!** Rubric grades
    can be manually overwritten.

General feedback
~~~~~~~~~~~~~~~~~~~

In addition to the new ways of giving feedback in CodeGrade, conventional
general feedback can be given too. Press the :fa:`pencil-square-o` button to
give and save general feedback.

Code Viewer settings
~~~~~~~~~~~~~~~~~~~~~

Like your favourite editor, the Code Viewer provides numerous settings to **fit your preferences**.
Click :fa:`cog` to change:

- Whitespace visibility

- Syntax highlighting

- Code font size

- Dark/light theme

- Amount of context lines

Feedback overview
~~~~~~~~~~~~~~~~~~~~

In the "Feedback overview" tab you can find an overview of the general feedback
and all the inline feedback given on a submission. The feedback overview is
shown automatically when an assignment’s state is set to **“Done”**. The amount
of lines displayed before and after each inline comment can be changed with the
"Amount of context" option in the Code Viewer settings. This is especially
useful for students to identify the types of mistakes they make most often.

Diff overview
~~~~~~~~~~~~~~~~

The "Diff overview" tab gives an overview of the differences between the
submitted work and a teacher’s revision. The amount of lines displayed before
and after each part that is different can be changed with the "Amount of
context" option in the Code Viewer settings.
