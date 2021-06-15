.. _setting-up-autotest:


Setting up AutoTest
================================================

.. deprecation_note:: /for-teachers/creating-automatic-tests

If you want to automatically grade your assignment, you can use AutoTest to do
so. AutoTest will automatically fill in rubric categories by running tests
on submissions. These tests are run automatically on our secure and reliable
AutoTest servers in the cloud.

1. Go to the **Assignment Management** page by clicking on the :fa:`cog` icon.

2. Navigate to the **AutoTest** page.

3. Firstly, let's setup the AutoTest run:

    a. Select when to make the results visible.

       - **Immediately**: let students view the results immediately after
         uploading, this is known as Continuous Feedback.
       - **When assignment is done**: let students view the result after the
         assignment state is set to done, just like any other feedback.

    b. Select the rubric calculation mode.

       - **Minimum**: a category's item will be chosen when the lower bound of
         this item is reached (e.g. when a category has 4 items and 75% of the
         tests succeed, the maximum item is filled in).
       - **Maximum**: a category's item will be chosen when the upper bound of
         this item is reached (e.g. you need 100% passed tests to have the
         maximum item filled in).

    c. Select a preferred revision.

       - **Student**: AutoTest is always run on the code the student has
         submitted.
       - **Teacher**: AutoTest is run on the teacher's revision of the code if
         it is available. Otherwise AutoTest is run on the student's
         submission.

    d. Upload your fixtures (this could be unit tests, setup scripts or
       anything else you need).  These fixtures will be available through the
       ``$FIXTURES`` directory.
    e. *Optionally* input a global setup script to run, for example to install
       packages you might need. :ref:`Click here <autotest-setup>` to see which
       packages are installed by default.
    f. *Optionally* input a per student setup script to run, for example to
       compile the students' code. Do all of your global setup in the global
       setup script, as this speeds up the AutoTest run.

4. Add a level to put your AutoTest categories in.

    .. note::
        For most use cases just one level is enough to do all your automatic grading with.

5. Add your AutoTest categories.

    .. toctree::
        :maxdepth: 1

        Add IO tests <setting-up-iotest>
        Add Run Program tests <setting-up-runprogramtest>
        Add Capture Points tests <setting-up-capturepointstest>
        Add Checkpoints <setting-up-checkpoints>
        Add Unit Tests <setting-up-unittest>
        Add Code Quality tests <setting-up-codequalitytest>


Now that AutoTest is set up, you can run it. Simply press the *run* button to
start the AutoTest run.
