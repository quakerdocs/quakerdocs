.. _guide_git_uploads:

Set up Git uploads for a CodeGrade assignment
=======================================================

.. deprecation_note:: /for-teachers/configuring-your-assignment/set-up-git-uploading

It can be very desirable or convenient to allow students to hand in to
CodeGrade directly via Git. Learning to work with Git is often a learning
goal for students and combining this with CodeGrade's features makes it very
well suited for education.

To set up Git submissions for your CodeGrade assignment, follow the steps below:

1. Go to the **Assignment Management** page for the assignment you want to enable git submissions for by clicking on the :fa:`cog` button.

2. Under the **General** tab, locate the **Allowed upload types** section.

3. Select the **GitHub/GitLab** checkbox to enable submissions via Git.

4. *Optionally*, deselect the **File uploader** checkbox to **only** allow students to submit via Git and not have an additional file uploader present on the hand-in page.

You have now enabled Git submissions for your CodeGrade assignment. Students
will be shown instructions on configuring their Git repository to work together
with CodeGrade, by setting up a *deploy key* and *webhook*. After setting this
up correctly, students' work will be uploaded to CodeGrade with every
``git push`` they execute. Encourage students to set this up before starting to
work on the assignment, so a nice history of submissions is created in CodeGrade.

.. warning::

    Git submissions work together with all of CodeGrade's features **except Hand-in
    Requirements.** Utilize i.e. CodeGrade Continuous Feedback to still give the
    students immediate feedback for every ``push``.

.. warning::

    CodeGrade has a size limit on student submissions. Exceeding this size limit
    will result in a warning message when regularly handing in, but not when
    using git to upload. If a student exceeds this limit, files exceeding the
    limit are silently deleted. This very rare case does result in a
    ``cg-size-limit-exceeded`` file to show up in the Code Viewer.

.. note::

    Want to see how your students use Git or even assess this automatically? The
    ``.git`` folder containing all information is accessible in the student
    submission to be inspected in our Code Viewer or assessed in AutoTest, run
    ``git fetch --unshallow`` to make sure the information is complete. You
    can also click on the *Github* or *GitLab* link to directly access the
    student repository.

.. note::

    If your CodeGrade assignment is set up as a Group assignment, all members
    of the group will have the same *deploy key* and *webhook* and can hand in
    for the whole group using Git in the same way they would for an individual
    assignment. **All members of the group will still have to open the CodeGrade
    assignment at least once in their LMS for this configuration to be
    generated! (This does not apply to stand-alone CodeGrade usage)**
