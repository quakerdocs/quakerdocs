Changelog
==========

.. deprecation_note:: /changelog


Version *Next*
--------------

**Released**: TBD

Removals
^^^^^^^^
API
***
- The option to incrementally fill in rubrics has been removed. You should
  now do a single request with all the selected rubric items for a submission
  with the ``PUT /api/v1/submissions/<submission_id>/rubricitems/`` to update
  the rubric result.

Version Nobel.2
----------------

.. json_include:: ../../release_notes.json
   :prepend: **Released**:
   :path: Nobel.2/readable_date

.. json_include:: ../../release_notes.json
   :path: Nobel.2/message

Features
^^^^^^^^^

- We now publish a library to consume our API, check it out on
  `PyPi <https://pypi.org/project/codegrade/>`_.

- Next to the original hard deadline, you can now also add a "lock date" after
  this, allowing you to make the deadline "soft".

- We've added a utils module within AutoTest (``cg_at_utils``). Using the
  ``CG_IFNO`` data is now as easy as doing ``from cg_at_utils import CG_INFO``.

Updates
^^^^^^^

- Added support for the Populi LMS.

Fixes
^^^^^

- Fixed a rare bug where LTI 1.1 passback would fail if we encountered a
  redirect.

- Added a workaround for a Canvas LTI 1.3 grade passback bug.

- Fixed blockquotes in the markdown input fields.

- Fixed a bug that caused AutoTest description templates to not be copied when
  importing an AutoTest.


Version Nobel.1
-----------------

.. json_include:: ../../release_notes.json
   :prepend: **Released**:
   :path: Nobel.1/readable_date

.. json_include:: ../../release_notes.json
   :path: Nobel.1/message

Features
^^^^^^^^^
- Provide more accurate feedback by customizing the messages in AutoTest.

Updates
^^^^^^^^
- Improve UX for setting up AutoTest setup scripts, making it more clear when
  you haven't changed the input and what the time-limit is for the command.
- Make it possible to overwrite AutoTest fixtures without deleting the old
  fixtures with the same name first.
- Automatically open the first subdirectories (those corresponding to AutoTest
  categories) in the AutoTest output file tree.
- We've added a tenant system to make our service even better. When logging in
  you now have to select your instance.

Fixes
^^^^^^

- Fix rare CSV export bug where exported data might be outdated if you didn't
  refresh the page since the last update.


Version Nobel
---------------------

.. json_include:: ../../release_notes.json
   :prepend: **Released**:
   :path: Nobel/readable_date

.. json_include:: ../../release_notes.json
   :path: Nobel/message

Updates
^^^^^^^^
- Add a limit to the maximum amount of plagiarism cases a single run can
  generate.
- Improve error messages when the server is overloaded.

Fixes
^^^^^^
- Never hyphenate code. When wrapping lines it could happen that code was
  hyphenated in the CodeViewer.

Removals
^^^^^^^^
API
***
- The option to get an entire course when getting an assignment has been
  removed. You should now request the course using the
  ``/api/v1/courses/<course_id>`` route to retrieve this course. The
  ``course_id`` is given when requesting an assignment.
- A plagiarism cases will no longer contain the two linked assignments. They do
  contain the two linked assignment ids (under the ``assignment_ids`` key), and
  the plagiarism run contains a lookup from assignment id to an assignment like
  object.
- When requesting all courses using the ``/api/v1/courses/`` route we will no
  longer provide the name of the role that the current user has in this
  course. Please either use the ``/api/v1/permissions/`` route to retrieve your
  own permissions, or the ``/api/v1/courses/<course_id>/users/`` to retrieve the
  role of a user.

UI
***
- Linters have been moved to AutoTest (AutoTest Quality Comments). The new
  integration allows for more flexibility and grading based on linter output.


Version Mosaic.3
-----------------

.. json_include:: ../../release_notes.json
   :prepend: **Released**:
   :path: Mosaic.3/readable_date

.. json_include:: ../../release_notes.json
   :path: Mosaic.3/message

Updates
^^^^^^^^^

- More descriptive error message when launched with LTI 1.3 without an
  assignment name.
- Make sure deleted submissions are ignored for calculating the analytics.

Fixes
^^^^^^^^^^
- Ignore empty "branch" parameter in webhook payload URLs.
- Fix crash on analytics page.
- Fix wrong rubrics being cleared when restarting an AutoTest result.


Version Mosaic.2
-----------------

.. json_include:: ../../release_notes.json
   :prepend: **Released**:
   :path: Mosaic.2/readable_date

.. json_include:: ../../release_notes.json
   :path: Mosaic.2/message

Features
^^^^^^^^^^^

- Rubric improvements. The rubric editor
  had a makeover: you can now view multiple categories at the same time, it is
  possible to reorder categories, and you can use markdown in both the category
  and item descriptions.
- AutoTest Code Quality comments. AutoTest has a new
  step type designed for linters. You can now place line comments within
  AutoTest and deduct points based on the amount of lines. We've integrated some
  popular linters, but it is also possible to create your own custom linters.

Updates
^^^^^^^^^^^^^^^^^^^^

- Expand inline links in markdown viewer. When you use http
  or https URLs in your markdown feedback, they are automatically turned into
  clickable links.
- It is no longer possible for students to edit their submissions in the filesystem. Students are
  now no longer allowed to edit their submissions using the CodeGrade
  filesystem. We can now guarantee that the student revision of a submission
  never changes.
- The API documentation has been revamped. This makes it easier
  for to start using our API. Please note that we haven't migrated all routes
  just yet, if you are missing a route please let us know!
- The Jupyter Notebook viewer now supports more output types and colors. If a Jupyter Notebook
  contains ANSI colored output we will display these colors in all their glory.
- When hiding inline feedback this setting is now saved when switching files. When you
  hide inline feedback using the preference settings on the submission page,
  this is now saved when switching between files and submissions.

Deprecations
^^^^^^^^^^^^
UI
***
- The linters integration has been deprecated. The new AutoTest Quality Comments
  bring all the advantages, and also allow you to give a grade based on the
  output of the linter.

Version Mosaic.1
-----------------

.. json_include:: ../../release_notes.json
   :prepend: **Released**:
   :path: Mosaic.1/readable_date

.. json_include:: ../../release_notes.json
   :path: Mosaic.1/message

Features
^^^^^^^^^^^^^^^^^^^^

- Add Sakai support. Full LTI integration
  with Sakai.
- Add support for SSO. CodeGrade now supports
  SSO leveraging the SAML2.0 protocol, allowing even better integration.
- Add CodeGrade Exam Mode. CodeGrade now has
  even better support for exams, allowing you to schedule the start of your
  exam, and making it possible to do exams for LTI courses without LMS access.
- Add import of hand-in requirements. You can now import the
  hand-in requirements of other assignments that you have access to.
- Add course archiving. You can now archive
  old courses, hiding them from students and cleaning your own homepage.

Updates
^^^^^^^^^^^^^^^^^^^^

- Use the same icons from the "Capture Points" AutoTest step for the "Unit
  Test" step.
  The "Unit Test" step would always use the green checkmark if the step did not
  crash, but now the icon depends on the score achieved.
- Make the peer feedback counters for students more clear. This changes the
  counters with the number of comments students have given to their peirs to be
  clearer and give more detailed information.
- Remove bin size "year" for the "Students submitted on" graph in the analytics
  dashboard.
  The years option did not work very nicely because it didn't use the correct
  labels, and it is unclear what the start of a bin should be, so it has been
  removed as it isn't really useful in a context where an assignment takes less
  than a year.
- Add rate limiting to login route. Make it impossible to
  bruteforce someone's password by sending infinite requests to the login
  route.
- Show more output in the Unit Test step. When a test case contains
  a ``<system-out>`` or ``<system-err>`` node its contents will now also be
  displayed in the output of the step.
- Renaming courses. It is now possible to
  rename existing courses.

Deprecations
^^^^^^^^^^^^
API
***
- The option to get an entire course when getting an assignment has been
  deprecated. You should now request the course using the
  ``/api/v1/courses/<course_id>`` route go retrieve this course. The
  ``course_id`` is given when requesting an assignment. If you still use the old
  behavior you will get a warning, you can already opt-in to the new behavior by
  providing ``no_course_in_assignment=true`` in the request arguments.
- When requesting a plagiarism case we have deprecated getting the two linked
  assignments within the plagiarism case object. The case will now contain the
  two linked assignment ids (under the ``assignment_ids`` key), and the
  plagiarism run contains a lookup from assignment id to an assignment like
  object. If you still use the old behavior you will get a warning, you can
  already opt-in to the new behavior by providing
  ``no_assignment_in_case=true`` in the request arguments.
- When requesting all courses using the ``/api/v1/courses/`` route getting
  name of the role that the current user has in this
  course has been deprecated. Please either use the ``/api/v1/permissions/``
  route to retrieve your own permissions, or the
  ``/api/v1/courses/<course_id>/users/`` to retrieve the role of a user. If you
  still use the old behavior you will get a warning, you can already opt-in to
  the new behavior by providing ``no_role_name=true`` in the request arguments.


Version Mosaic
---------------

**Released**: July 21st, 2020

With CodeGrade Peer Feedback it is now possible for students to review code of
other students, allowing them to learn from each other. Furthermore, it is even
easier to integrate existing unit tests in AutoTest, by utilizing the new "Unit
test" step type.

Features
^^^^^^^^^^^^^^^^^^^^

- Add "Unit Test" AutoTest step. This new AutoTest
  step type supports all testing frameworks that can output their results the
  JUnit XML format. The results are shown to the student  in an intuitive
  overview.
- Make it possible to run AutoTest on the teacher revision instead of the
  student submission, if it is available..
- Allow test submissions before the deadline. This may be useful
  when setting up a course without knowing the deadline yet in LMSes that
  support deadline synchronization, for which impossible to change the deadline
  from within CodeGrade.
- Add Peer Feedback feature. When peer feedback
  is enabled for an assignment, students can give each other feedback after the
  deadline of an assignment has passed.

Updates
^^^^^^^^^^^^^^^^^^^^

- Automatically focus the percentage input in continuous rubric rows.
- Make it easier to upgrade from LTI 1.1 to LTI 1.3.
- Add more rubric category information to the rubric analytics graphs.
- Do not automatically hide the general feedback popover after saving the
  general feedback or interacting with the page.
- Add the year to course names in the sidebar if there are other courses with
  the same name.
- It is now possible to restart the AutoTest run for a single student.

Fixes
^^^^^^^^^^^^^^^^^^^^

- Fix IPython ``execute_result`` cell outputs.
- Add missing newline at the end of symbolic link replacement files.
- Miscellaneous fixes.

Version *LowVoltage.1*
----------------------

**Released**: June 10th, 2020

With our new Feedback Sidebar, you can now view all previous feedback from
a student in the course, while grading the current submission. It is now also
possible to get submission metadata in AutoTest, for instance to automate late
day penalties. Finally, we have upgraded CodeGrade to the newest version of
LTI: LTI 1.3 Advantage!

Features
^^^^^^^^^^^^^^^^^^^^

- Course feedback. Adds an overview of
  all the feedback a student received over an entire course. Teachers have
  access to this overview on the submission page in the same location as the
  file tree. For students there is an extra button on the submissions page.
- Improve plagiarism document rendering. Matching blocks of
  code can now be rendered side by side, the amount of context lines before and
  after each match is configurable, and it is possible to export to a docx
  file.
- Add LTI 1.3 implementation. This makes the
  integration in the LMS even better, allowing better workflows for group
  assignments and easier assignment creation.
- Include submission information in AutoTest environment. Some information
  about a submission is now available in AutoTest as a JSON object that is
  stored in an environment variables. This is useful to automatically subtract
  points based on the submission date and deadline, or to generate a unique
  input for each submission or student.

Updates
^^^^^^^^^^^^^^^^^^^^

- Use Bootstrap-Vue toasts instead of vue-toasted,

Fixes
^^^^^^^^^^^^^^^^^^^^

- Fix AutoTest result being in state "done" while it has steps that are in
  state "waiting to be started"
- Remove "Add filter" button from analytics dashboard.
  The button was confusing when splitting a filter, and since there already is
  another button to add new filters we removed it.
- Fix notification sorting order. Unread
  notifications are now always sorted before read notifications.
- Miscellaneous fixes.

Version LowVoltage
-------------------

**Released**: April 15th, 2020

You can now view assignment statistics on the Analytics Dashboard, giving you
insight into student performance. Students can now also comment on their own
code, and they can reply to comments placed by teachers.

Features
^^^^^^^^^^^^^^^^^^^^

- Analytics dashboard. The analytics
  dashboard is a new page with various statistics about an assignment. It gives
  teachers insights in how students are performing on the assignment and where the
  assignment may be improved.
- Inline feedback replies. It is now possible
  to reply to inline feedback, which makes distance learning easier to do with
  CodeGrade. This update also adds markdown formatting to inline feedback, and
  notifies you when you have received new replies.
- Contact student button. This makes it
  possible for teachers to send emails to students of a submission, or to
  multiple students in a course.


Updates
^^^^^^^^^^^^^^^^^^^^

- Make usernames case insensitive. This reduces
  ambiguity in which user you are dealing with, as well as making it easier to
  login because you do not have to remember if you used an uppercase or not
  when you registered.
- Various internal improvements. This makes it easier
  to improve CodeGrade in the future.
- Plagiarism support for newer versions of Java. You can now use the Plagiarism
  checker for newer versions of Java.

Fixes
^^^^^^^^^^^^^^^^^^^^

- Make sure that empty markdown files show a useful error.

Version Knoet.3
-----------------

**Released**: March 16th, 2020

You can now render HTML pages submitted by students right inside CodeGrade,
allowing you to preview webpages or test Javascript more easily than ever.

Features
^^^^^^^^^^^^^^^^^^^^

- Make it possible to render html pages: It is now possible to
  render HTML pages inside CodeGrade.
- Make the HomeGrid easier and faster to use: We now sort the
  courses on the HomeGrid based on the creation date of the courses, and courses
  with duplicate names can now be more easily identified as the creation date of
  the course will be appended to the name.


Updates
^^^^^^^^^^^^^^^^^^^^

- Upgrade bootstrap-vue.
- Show confirmation when rubric has rows without item with 0 points.
- Update threshold when relative time starts using days.
- Disable plagiarism export button when no cases selected.
- Give a better indication when an AutoTest step is hidden.
- Various performance improvements: We've increased
  performance of various API routes, and added pagination and infinite scrollers
  to the HomeGrid, Submissions list and users manager to improve the first
  render speed.
- Start using timezones everywhere when dealing with datetimes.

Fixes
^^^^^^^^^^^^^^^^^^^^

- Do not discard changed rubric viewer when saving general feedback: The previous version
  contained a bug that when you saved the general feedback while you had a
  changed rubric the changes in the rubric were discarded.
- Fix downloading submissions with reserved chars in their name.
- Fix student count in submission list.

Version 1.19.0 (Knoet.2)
-------------------------

**Released**: January 30th, 2020

You can now add Continuous Rubric Categories, which can score anywhere on a
continuous scale and work great with AutoTest. You can also now set student
submission limits and a cool off period.

Features
^^^^^^^^^^^^^^^^^^^^

- Continuous rubric categories: this new type of
  rubric category can be used to give points anywhere on a scale from 0 to a
  configurable amount of points. This behavior maps better to certain types of
  AutoTest categories, such as categories containing only "capture points"
  steps. Rubrics can contain a mix of discrete and continuous categories and
  both can still be used for AutoTest.
- Make it possible to limit the amount of submissions: the amount of
  submissions can be limited in two ways:

  1. A maximum total amount of submissions for an assignment.
  2. A cool-off period: an amount of time a student must wait before they can
     submit again.
- Separate feedback permissions: the
  `can_see_grade_before_done` permission was used for all types of feedback
  students would get. New `can_see_user_feedback_before_done` and
  `can_see_linter_feedback_before_done` permissions make it possible to show
  these types of feedback before an assignment is set to done while still
  hiding others.

Minor updates
^^^^^^^^^^^^^^^^^^^^

- Add warning when creating a wrong external tool link in Canvas: Canvas has multiple
  ways to integrate external tools, some of which leave CodeGrade unable to
  communicate correctly with it. This update displays a message when this
  happens.

Fixes
^^^^^^^^^^^^^^^^^^^^

- Use the most privileged LTI role available.
- Fix float matching for AutoTest capture points test.

Version 1.17.0 (Knoet.1)
--------------------------

**Released**: December 20th, 2019

The hand in page for students has been completely redesigned, making it simpler
and easier to use. You can now import AutoTest configurations and the ESLint
linter is now available.

Features
^^^^^^^^^^^^^^^^^^^^

- Submissions page redesign:
  the hand in page has been completely redesigned and simplified for students.
  Students now see a few clearly visible big buttons to either view a previous submission,
  view the rubric, upload files, use groups or get git instructions.
- Add ESLint as a linter option:
  you can now use the ESLint linter.
- Make it possible to delete assignments:
  assignments can now be deleted from the Assignment Management Page on the general tab.
- Make it possible to copy AT config:
  you can now import AutoTest configurations from other assignments. This will also copy
  the rubric.
- Add course registration link:
  for standalone courses, you can let users register via a unique URL. You can
  set this up on the Course Management Page.

Minor updates
^^^^^^^^^^^^^^^^^^^^

- Update git instructions:
  the git instructions have been updated to be more compatible with git GUIs. We've
  also added a button to the last step to check if submitting works correctly.
- Stop persisting access tokens in LTI:
  you're now only logged in persistently when pressing the "New Tab" button. This fixes some issues
  where users were always logged in via LTI.

Fixes
^^^^^^^^^^^^^^^^^^^^

- Set groups of user in AutoTest run.
- Fix the default configurations for Checkstyle.
- Stop registering AT jobs at the broker if there are no submissions.
- Fix deadlock that would occur when attaching failed.
- Use a blob storage for the jwt data instead of passing it in the request.

Version 1.16.2 (Knoet)
--------------------------

**Released**: November 27th, 2019

It is now possible to hand in via GitHub or GitLab. You can now also write
files back from AutoTest to the Code Viewer to ease manual grading.

Features
^^^^^^^^^^^^^^^^^^^^

- Make it possible to hand in submission through GitHub+GitLab:
  this makes it possible for students to automatically hand in submissions by pushing to
  GitHub or GitLab. Each student gets a unique URL, SSH public key and secret which
  can be used to configure a deploy key and webhook.
- Add AutoTest output directory:
  AutoTest scripts can now write files to the ``$AT_OUTPUT`` directory. Files written
  to this directory are synced with CodeGrade and can be viewed in the Code Viewer.
- Make it possible to check plagiarism in Jupyter Notebooks:
  You can now check for plagiarism in Jupyter Notebooks.
- AutoTest Best Practices in docs:
  there is now a Best Practices for AutoTest guide in the documentation.

Minor updates
^^^^^^^^^^^^^^^^^^^^

- Add year to old assignments dropdown:
  this makes it easier to distinguish between courses with the same name.
- Add option to hide inline feedback:
  in the code viewer settings you can now optionally hide inline feedback.
- Hide hidden fixtures from students:
  the name of hidden fixtures are now also hidden for students making it harder for them to know they exist.
- Improve the first render speed for AutoTest:
  AutoTest now loads much faster.

Fixes
^^^^^^^^^^^^^^^^^^^^

- Fix giving feedback on PDF files in edge.
- Fix incorrect late submission clock.
- Fix race condition filling in rubric with AutoTest.
- Fix getting latest submissions in combination with groups.
- Fix typo for max time command in front-end.
- Fix permissions fixtures directory.
- Fix IO substep timers.
- Fix feedback area author width.
- Reduce amount of requests when loading plagiarism runner.
- Only open the feedback area on a left click in the code viewer.
- Cache code in the frontend.
- Don't show AutoTest popover on page load.
- Stop loading the rubric and graders twice on the management page.


Version 1.13.0 (JungleJoy.4)
--------------------------------

**Released**: October 11th, 2019

AutoTest and Continuous Feedback cooperate even better with this release. Tests
are always run immediately after handing in, and even fill in the rubric
directly when possible. Teachers can still choose when to make results visible
to students.

Features
^^^^^^^^^^^^^^^^^^^^

- Merge AutoTest & Continuous Feedback:
  AutoTest and Continuous Feedback are now integrated together. AutoTest
  automatically runs on all submissions and new submissions and you can choose
  whether to make the results visible to students immediately (Continuous
  Feedback) or only after the assignment state is set to done.
- Brightspace support:
  CodeGrade now fully supports Brightspace.

Minor updates
^^^^^^^^^^^^^^^^^^^^

- Improve scrolling on the submission list page:
  on small screens the rubric sometimes overlaps with the upload field, this has
  now been improved.
- Create a new config option to add an admin user to each course:
  it is now possible to add an admin user to courses automatically, making
  technical support easier.
- Show confirm message when overwriting an existing snippet.
- Show warning when rendering extremely large files.
- Make it possible to submit comments containing the null byte.
- Make it possible to see the plagiarism table without manage permission:
  this makes it easier to give TAs the permission to see plagiarism cases,
  without them being able to edit the plagiairism run.
- The CodeViewer is faster, and works better when dealing with large files.

Fixes
^^^^^^^^^^^^^^^^^^^^

- Fix race condition in editable rubric editor.
- Fix late submission warning.
- Fix hand in requirements bugs:
  sometimes a file was matched by multiple rules and there was a bug with empty directories when using the deny all policy.
- Fix race condition when creating unassigned runners.
- Fix plagiarism overview when missing permissions on other courses.


Version 1.11.11 (JungleJoy.3)
-----------------------------

**Released**: September 13th, 2019 *(we blame all bugs on Friday the 13th)*

AutoTest and Continuous Feedback are now more reliable and efficient by fixing
many small bugs and tweaks in the back-end. Additionally, a diff-viewer is added
to the output of IO tests.

Features
^^^^^^^^^^^^^^^^^^^^

-  Add diff view to IO test: Adds a
   difference viewer to the IO test in AutoTest and Continuous Feedback.
-  Make it possible to use CF after a final run: enable
   starting Continuous Feedback after an AutoTest run finished.


Minor updates
^^^^^^^^^^^^^^^^^^^^

-  Add Test Submissions:
   makes it possible for teachers to more easily upload test submissions to test
   Continuous Feedback or Hand in Requirements configurations.
-  Add guide for students:
   Add a new student guide to the documentation.
-  Remove log pushing functionality: logs were
   not useful during debugging. This reduces the amount of threads on the
   machine too.
-  Add more info about the job in the broker panel: adds
   course name, assignment name and type of job to the internal broker panel.
-  Show failed auto tests as failed: better
   communicate the output of Capture Points tests. Zero points results in
   failing, full points in passing and anything in between in a ``~``.
-  Improve broker panel: adds
   colors, limits the amount of rendered jobs and runners and adds function to
   shutdown runner instead of terminating.
-  Improve Assigned to me filter: disables
   the checkbox entirely for users without submissions and makes manually
   assigning to oneself more smooth.
-  Improve AutoTest: this
   makes AutoTest and Continuous Feedback more reliable and efficient:

   - Fix deadlock when starting commands
   - Improve the way command timeouts are handled
   - Add timeouts to all requests to the server
   - Improve handling of multiple submissions

-  Hide assignments without deadline in sidebar top: assignments
   without deadlines were displayed above assignments with a deadline in the
   upcoming assignments list. This is reversed now.


Fixes
^^^^^^^^^^^^^^^^^^^^

-  Fix rubric item deletion bug:
   fixes the bug where lest rubric items could be removed by accident.
-  Fix by waiting for systemd to be done booting:
   fixes the rare bug that AutoTest runners would never start.
-  Minor fixes for student submission page: this
   changes the grade placeholder when no grade is given yet and removes
   unavailable buttons.
-  Make it possible to go back from group page: adds a
   back button and clickable assignments to this page.
-  Fix editing feedback in IPython notebook files: fixes
   the broken line feedback for IPython notebook files.
-  Count the achieved points of capture_points steps in suite percentage: fixes the
   bug that points for capture points tests were not counted.
-  Fix very long waiting on attach bug.
-  Make sure markdown rendering is he same as in IPython Notebooks.
-  Fix group management loaders in LMS.



Version 1.10.3 (JungleJoy.2)
-----------------------------

**Released**: August 28th, 2019

It is now significantly more efficient to run AutoTest or Continuous Feedback by
a big improvement in our back-end. Additionally, our latest update adds further
improvements to CodeGrade and fixes several minor and rare bugs.

Features
^^^^^^^^^^^^^^^^^^^^

-  Use multiple runners: make
   AutoTest or Continuous Feedback more efficient by allowing multiple runners
   to work on one run.
-  Only show latest submissions by default: make
   loading of submission(s) pages more efficient by only loading latest
   submissions by default, which especially is a problem with continuous
   feedback which can cause high amounts of attempts per student. Additionally
   adds an improved dropdown to switch between submissions of one student.


Minor updates
^^^^^^^^^^^^^^^^^^^^

-  Improve popovers for locked rubric rows:
   improves presentation of rubrics on more pages and adds popover to the whole
   rubric instead of only the lock icon.
-  Increase indentation of files in the file tree.
-  Improve scrolling to match near end in plagiarism detail: make it
   possible to align plagiarism matches even if one is near the bottom of the
   file.
-  Remove confirmation to delete feedback when FeedbackArea is empty: make it
   quicker to remove empty inline comments by removing confirmation dialog.
-  Use a tail of output use for custom output matching: capture
   points tests have a cap on the output of the command. Now the points are
   always captured from the tail of this output.
-  Minor AutoTest setup script improvements: make
   Continuous Feedback setup script output visible to students and improve the
   setup scripts popover texts.
-  Move Jplag languages to the config: adding
   new languages to our plagiarism detection is easier now, as it does now not
   need modifications in the CodeGrade source code.
-  Add pagination to the AutoTest run overview: if there are too
   many results for an AutoTest run the results will be paginated, which
   decreases loading time and makes the page responsive.

Fixes
^^^^^^^^^^^^^^^^^^^^

-  Fix general feedback overflow:
   fixes the bug where too long general feedback causes an overflow.
-  Fix race condition when starting an AutoTest run:
   fixes the UI glitch that continuously reloads the student list.
-  Fix infinitely reloading a Continuous Feedback AutoTestRun.
-  Fix selecting text in the InnerCodeViewer.
-  Fix issue with inline feedback in exported CSV.
-  Return IO substep name and weight when no permission to view details: still
   display names of substeps of IO tests if these are hidden. Details do not
   show.
-  Make sure waiting on pid only starts after command is started.
-  Fix "Stop CF" button not working sometimes: fixes a
   very rare bug which would break the "Stop CF" or "Delete Run" buttons.
-  Clear store rubrics in the RubricEditor when they change: fixes the
   bug that required a refresh before a new rubric would show up on the
   submission page.
-  Use correct URL in group management component.
-  Lots of bugfixes and minor improvements: this fixes
   numerous small bugs, including:

   - Download files without posting them to the server first
   - Do the doc build in the unit build on Travis
   - Round number of decimals in AutoTest result modal header
   - Add percent sign to checkpoint inputs
   - Merge "Info" and "Output" tabs in AutoTest result

-  Fix a bug where multiple submisions of a user could be shown if they had the
   exact same date.


Version 1.9.0 (JungleJoy.1)
-----------------------------

**Released**: August 14th, 2019

You can now make sure students get near instant automatic feedback using our
new extension of AutoTest called Continuous Feedback. To better present
this feedback to students, we have redesigned the entire submission page to be
more intuitive.

Features
^^^^^^^^^^^^^^^^^^^^

-  Rewrite submission page: make overview
   page obsolete and allow easier access to AutoTest results and feedback.
-  Add initial implementation for Continuous Feedback: with Continuous
   Feedback, students receive near instant automatic feedback on every submission
   they hand in.
-  Add Scala as plagiarism option.

Minor updates
^^^^^^^^^^^^^^^^^^^^

-  Add *all_whitespace* option to IO test: add new
   option to IO tests to ignore all whitespace when comparing.
-  Update stop points to percentages: to better
   work together with possible disabled tests in Continuous Feedback, all stop
   or check points now work with percentages instead of points. (**not backwards
   compatible!!**)

   .. warning::
      Update is **not** backwards compatible. Previous stop / check points break
      if not updated to percentages.

Fixes
^^^^^^^^^^^^^^^^^^^^

-  Improve plagiarism export:
   fix non-escaped underscores and add option to output each listing on new page.
-  Change text on 'delete files' button when handing in.


Version 1.7.0 (JungleJoy)
-------------------------

**Released**: July 09th, 2019

You can now automatically grade code of students using our brand new feature
called *AutoTest*. This enables teachers to easily create test configurations
and students to automatically get insightful feedback.

Features
^^^^^^^^^^^^^^^^^^^^

- AutoTest is CodeGrade's new Automatic Grading Environment: with AutoTest you can
  automatically grade code of students and provide them with insightful
  feedback.

Fixes
^^^^^^^^^^^^^^^^^^^^

- Improve documentation: We are always
  pushing for the best documentation!
- Increase the speed of multiple routes and pages.
- Show error when negative grader weights are submitted.
- Further improve the way we handle too large archives.


Version 1.6.6 (Izanami.2)
-------------------------

**Released**: April 04th, 2019

You can now set up detailed hand-in requirements for your students,
create course snippets and the submission page is easier to and has more
information (including the possibility to upload multiple files).

Features
^^^^^^^^^^^^^^^^^^^^

-  Add a new version of the ignore file: this
   makes it possible to set detail hand-in requirements for students.
-  Allow uploading multiple files:
   students can now upload multiple files and archives.
-  Add course snippets:
   course snippets are shared between all teachers and ta's of a course.
-  Add Moodle support: full
   LTI integration with Moodle.
-  Add Blackboard support: full
   LTI integration with Blackboard.
-  Enhance documentation:
   better documentation which includes user guides.
-  Rewrite submission list page header: more
   information, including a better visible rubric for students.

Minor updates
^^^^^^^^^^^^^^^^^^^^

-  Edit snippets in modal: a
   better UI for adding snippets.
-  Add border when CodeGrade is loaded in an iframe in Canvas: this
   makes it more clear where CodeGrade begins and Canvas ends.
-  White background for sidebar when not in dark theme: this
   makes the light mode more beautiful.
-  Improve the way rubric maximum points are presented: added
   warnings and improved the UI, so the feature is not misused.
-  Make it possible to filter submissions by member of the group.
-  Increase the default value used for minimal similarity for jplag:
   changed it from 25 to 50, making sure users don't get too much cases
   by default.
-  Add multiple file uploader to documentation.
-  Update documentation to apply to new snippet management UI.
-  Improve filtering the course users:
   increased the efficiency of the filtering.

Fixes
^^^^^^^^^^^^^^^^^^^^

-  Make sure duplicate filenames are detected and renamed.
-  Show when user has no snippets.
-  Set default deadline time to 23:59.
-  Fix new tab button position in sidebar.
-  Fix home page logo position.
-  Fix header text color in dark theme.
-  Fix file tree resizer z-index.
-  Rename "Old password" to "Current password".

Version 1.3.29 (Izanami.1)
--------------------------

**Released**: March 09th, 2019

Along with many UI improvements and bug fixes, you can connect grading divisions
between assignments and import rubrics from previous assignments.

Features
^^^^^^^^^^^^^^^^^^^^

- Make it possible to connect assignment divisions: This makes it possible
  to have the same TAs grade the same students over the duration of the entire
  course.
- Make it possible to import rubrics from other assignments.
- Improve UI/UX for running linters: Logs of the linter
  runs on the individual submissions can now be viewed.
- Enable use of multiple LTI providers: Soon we will be able
  to connect with Blackboard, Moodle, Brightspace, and others!
- Make it possible to resize the filetree.

Minor updates
^^^^^^^^^^^^^^^^^^^^

- Make it impossible to list all users on the system by searching: All users on the
  system could be listed by almost anyone.
- Confirm clearing a rubric: Instead of requiring
  the user to click the submit button for the grade to reset a rubric, the new
  submit button confirmation popover is used to confirm the action.
- Rewrite SubmitButton component: Buttons will
  not change size anymore, and when an error occurs the button will wait for
  the user to close the message, instead of the error message disappearing
  after a few seconds, not giving the user a chance to read the entire thing.
- Change sidebar login icon: The icon was ugly and
  its meaning not very obvious.
- Add button to open in new tab in LTI: It was unclear that
  the logo in the sidebar would open CodeGrade in a new tab, so an extra button
  has been added.
- Remove show password button: The button on the
  right side of the password inputs has been removed, as it is not very useful.
- Show progress for plagiarism runs: Plagiarism runs could
  take quite some time but didn't show the progress until they quit
  successfully or crashed.
- Make it possible to search the homegrid.
- Make it possible to download the plagiarism log.
- Add warning on permission management page: When permissions are
  changed it shows a notification that the page must be reloaded for the
  changes to take effect.
- Add a release notifier on the home grid: Whenever a new version
  of CodeGrade is installed, a notification will be shown on the home page with
  a link to this changelog.

Fixes
^^^^^^^^^^^^^^^^^^^^

- Add formatted_deadline property to the course store for assignments.
- Make sure permissions are removed on logout.
- Add smaller logo on standalone pages.
- Make sure only plagiarism runs which have finished can be viewed.
- Make sure password reset works and logs in user.
- Make sure error message is correct when empty archive is uploaded.
- Make sure we don't mutate store objects in the rubric editor.
- Make sure order of submissions is stable.
- Fix large amount of trailing zeros in the rubric viewer.
- Prevent error in console when not logged in on page load.
- Make sure 500 never occur because of ``__maybe_add_warning`` function.
- Merge the loaders of the plagiarism runner.
- Fix bug when reloading assignments on submission page.
- Add link to about us page in the footer.
- Clearer plagiarism similarity placeholder.
- Reserve some extra special filenames.

Version 1.2.19 (Izanami)
------------------------

**Released**: February 07th, 2019

Features
^^^^^^^^^^^^^^^^^^^^

- Group assignments: With this release
  we have added group assignments. It is possible to create groups, share
  them between assignments, and submit as a group. Groups can be given
  a nice name, that is easily remembered by the TA.
- Add support for 7zip as archive format
- Make late submissions stand out: Submissions that have
  been handed in after the deadline are highlighted in the submissions list.
- Make it possible to display IPython notebooks: CodeGrade now renders
  handed in IPython notebooks in the web interface instead of showing a JSON
  blob. Additionally, markdown files are also rendered. Teachers can place
  comments in both types of files, as well as on image files now. This also
  adds a message when a file does not end in a newline character.

Minor updates
^^^^^^^^^^^^^^^^^^^^

- Show message when uploaded file is empty: When a file is empty,
  it wouldn't show up at all in the code viewer. This changes it to show
  a message, indicating that the file is empty.
- Make the user selector more clear: The user selector now
  shows a magnifying glass, indicating that the user can type to search for
  users.
- Use flatpickr datetime picker instead of native: Date/time inputs have
  been changed to use a date picker, so users of browsers besides Chromium can
  now also pleasantly select a date or time.
- Change icon for user in the sidebar

Fixes
^^^^^^^^^^^^^^^^^^^^

- Hide plagiarism providers when there is only one
- Make sure it is possible to ignore single files: When a student
  submitted a single file instead of an archive, the student would not be warned
  that the file was ignored by the assignment's CGignore file.
- Make sure confirmations work correctly when submitFunction is used
- Improve grade viewer: It was not possible to
  simultaneously submit a change to a rubric and override the grade calculated
  by the rubric.
- Various front-end UI fixes
- Various browser specific UI fixes

Version 1.1.4 (HereBeMonsters.3)
---------------------------------

**Released**: January 16th, 2019

Features
^^^^^^^^^^^^^^^^^^^^

- Add PMD and Checkstyle linters: Addition of two Java
  linters: PMD and Checkstyle. For security reasons, some restrictions on config
  apply. Please see the documentation for more details

-  Add snippet completion and selection: This
   makes it easier for users to use and add snippets.

Fixes
^^^^^^^^^^^^^^^^^^^^

-  Fix a bug hiding indentation on lines with linter errors: When
   linting lines with errors didn’t show indentation.
-  Fix dark special holiday logo.
-  Make it impossible to upload too large archives: This
   makes it way harder for users to bypass our restrictions to upload
   very large archives.
-  Various internal fixes and improvements.
-  Don’t apply “mine” filter when assigning first submission to self: When
   no submission had an assignee and you assigned yourself it filtered
   all other submissions directly.
-  Make sure the grade is updated when rubric is.
-  Improve worst case performance in some plagiarism cases.

Version 1.0.22 (HereBeMonsters.2)
----------------------------------

**Released**: November 21st, 2018

Features
^^^^^^^^^^^^^^^^^^^^

-  Enforce minimal password strength:
   CodeGrade now enforces a minimum password strength for all users. A
   warning is also shown if a user logs in with a password that doesn't
   adhere to the current requirements. We recommend all users to update
   their passwords if they receive such a warning.
-  Update course and assignment name on LTI launch: If
   the name of a course or assignment changes within your LMS this
   change is now copied in CodeGrade.
-  Do lti launch on grade result: When
   viewing new grades this will trigger an LTI launch. This means you
   will always be logged-in in CodeGrade with the current LMS user.
-  Show a loader instead of the delete button for plagiarism checks that
   are still running.

Fixes
^^^^^^^^^^^^^^^^^^^^

-  Only show register button when the feature is enabled.
-  Make it possible to create PDF manuals.
-  Fix plagiarism detail viewer:
   Because of a misplaced bracket it was not possible to view plagiarism
   cases.
-  Always do an initial grade passback: This
   reverts a change in version 1.0.0 which caused Canvas to not remove
   CodeGrade assignments from the todo list of students. By doing a LTI
   passback when students hand-in a submission the assignment should be
   removed from their todo list.
-  Various small logging fixes.
-  Redact emails of other users: This
   is a minor **breaking change**. When serializing a user an ``email``
   key was always sent including the email of every user. With this
   change the ``email`` key is only sent with the extended serialization
   of a user, and the value is changed to ``'<REDACTED>'`` for every
   user except the currently logged-in user. This prevents people in the
   same course from seeing each others email.
-  Improve speed of plagiarism route: By
   using the database in a more efficient way this route should become
   about twice as fast!
-  Various styling fixes.

Version 1.0.7 (HereBeMonsters.1)
--------------------------------

**Released**: November 12th, 2018

Features
^^^^^^^^^^^^^^^^^^^^

- Support files encoded as ISO-8859-1 (latin1) in the frontend.

Fixes
^^^^^^^^^^^^^^^^^^^^

- Make it impossible to override the special files of the CodeGrade
  filesystem.
- Various frontend fixes.
- Improve documentation.

Version 1.0.0 (HereBeMonsters)
------------------------------

**Released**: October 30th, 2018

Features
^^^^^^^^^^^^^^^^^^^^

-  Add Plagiarism checkers: It is now possible to check for plagiarism in
   CodeGrade. This enables privacy aware plagiarism checking. It is
   possible to use check against old CodeGrade assignment and upload
   base code and old submissions that are not in CodeGrade. For more
   information see our documentation.

-  Make it possible give grades higher than ten: Teachers can now
   indicate that students can receive a grader higher than 10 for an
   assignment, making it possible to create assignments with bonus
   points in CodeGrade. When using within LTI this requires a new LTI
   parameter.

   You should add the following to the ``<blti:custom>`` section of your
   canvas LTI config for CodeGrade:

   .. code:: xml

      <lticm:property name="custom_canvas_points_possible">
        $Canvas.assignment.pointsPossible
      </lticm:property>

Minor updates
^^^^^^^^^^^^^^^^^^^^

-  Change homepage to login screen:
   The homepage has been improved to show all your courses and
   assignments at a glance when logged in.
-  Use new logos: This updates our logo to the newest and
   greatest version!
-  Allow .tar.xz archives to be uploaded: This further improves
   the flexibility CodeGrade gives students when handing in submissions.
-  Fix infinite loop overview mode: In some combinations of
   permissions loading the overview mode resulted in an infinite loader.
-  Add general feedback tab to overview mode: This further
   decreases the chance that students will miss any of their feedback.
-  Improve speed of diffing by using another library: Viewing the
   diff between two large files is a lot faster!
-  Remove the option to automatically generate keys: It is no
   longer possible to generate the ``secret_key`` or ``lti_secret_key``
   configuration options. Please update your config accordingly.
-  Rewrite snippets manager: This rewrite should make creating,
   using, deleting and updating snippets faster and more reliable.
-  Drastically improve the experience of CodeGrade on mobile: It
   is now way easier to use CodeGrade on mobile.
-  Filter users in the user selector: When selecting users (when
   uploading for others, or adding to courses) only show users will be
   shown that can be selected.
-  Improve handling of LTI: A complete rewrite of LTI
   backend handling. This should improve the stability of passbacks by a
   lot. This also guarantees that the submission date in Canvas and
   CodeGrade will match exactly. This also adds a new convenience route
   ``/api/v1/lti/?lms=Canvas`` to get lti config for the given LMS
   (Canvas only supported at the moment).
-  Add items to the sidebar conditionally: Depending
   on what page you are you will get extra items in the sidebar to help
   quick navigation. Currently plagiarism cases and submissions are
   added depending on the page.
-  Start caching submissions: Submissions are cached in the
   front-end so changing between the codeviewer and submissions list is
   now way quicker.
-  Ensure all rubric rows have a maximum amount of >= 0 points: It
   is no longer allowed to have rows in a rubric where the maximum
   possible score is < 0. If you needed this to create rubrics with
   bonus categories simply use the ‘Max points’ option in the rubric
   editor. All existing rubrics are not changed.

Fixes
^^^^^^^^^^^^^^^^^^^^

-  Various small bugs in the sidebar
-  Add a minimum duration on the permission manager loaders: This
   makes it clearer that permissions are actually updated.
-  Throw an API error when a rubric row contains an empty header:
   This is a backwards incompatible API change, however it doesn’t
   change anything for the frontend.
-  Fix broken matchFiles function: This fixes a bug that
   files changed inside a directory would not show up in the overview
   mode.
-  Fix horizontal overflow on codeviewer: The codeviewer would
   sometimes overflow creating a vertical scrollbar when displaying
   files containing a large amount of consecutive tabs.
-  Check if an assignment is loaded before getting its course: In
   some rare cases LTI launches would fail be cause assignments were not
   loaded correctly.
-  Add structured logging setup: This makes it easier to follow
   requests and debug issues.
-  Fix general feedback line wrapping: Giving long lines as
   general feedback should be displayed correctly to the user now.
-  Add manage assignment button to submission list: It is now
   possible to easily navigate to the manage assignment page from the
   submissions list.
-  Start using enum to store permissions in the backend: Most
   routes will be faster by this design change.
-  Improve filetree design: It is now easier to spot
   additions, changes and deletion directly in the filetree.
-  Add ``<noscript>`` tag: An error message will be displayed when
   javascript is disabled.
-  Improve speed of filetree operations: Loading large filetrees
   is now way quicker by using smarter data-structures.
-  Add health route: It is now possible to more easily monitor the
   health of your CodeGrade instance.
-  Fix fontSize & contextAmount on submission page: Sometimes the
   fields would show up empty, this shouldn’t happen anymore!
-  Replace submitted symlinks with actual files: When a student
   uploads an archive with symlinks the student is warned and all
   symlinks are replaced by files explaining that the original files
   were symlinks but that those are not supported by CodeGrade.
-  Fix grade history popover boundary: The grade history would
   sometimes show up outside the screen, but no more!
-  Make it impossible to submit empty archives: A error is shown
   when a student tries to submit an archive without files.
-  Show toast when local-storage doesn’t work: When a user has no
   local-storage available a warning is shown so the user knows that
   their experience might be sub-optimal.
-  Show author of general feedback and line comments: The
   author of all general feedback and line comments is displayed to the
   user. Only users with the ``can_see_assignee`` permission will see
   authors.
-  Justify description popover text: The text in descriptions is
   now justified and their popups will only show when the ‘i’ is
   clicked.
-  Only submit rubric items or normal grade: In some rare cases
   overriding rubrics would result in a race condition, resulting in
   wrong case.
-  Redesign the download popover on the submission page: This new
   design looks way better, but you tell us!
-  Only show overview mode when you have permission to see feedback: When you don’t have permission to see feedback the overview
   mode will never be shown.
-  Various other performance improvements: We always strive for
   the best performance possible, and again in this release we increased
   the performance of CodeGrade!
-  Make sure codeviewer is full width on medium pages: This makes
   it easier to review and display code on smaller screens.
-  Use custom font in toasted actions: It is now always possible
   to close toasts, even when your font cannot display ‘✖’.

Version 0.23.21 (GodfriedMetDenBaard.2)
-----------------------------------------

**Released**: May 4th, 2018

Fixes
^^^^^^^^^^^^^^^^^^^^

* Make long rubric item headers show an ellipsis
* Fix sidebar shadow with more than one submenu level
* Make sure grade is updated when non incremental rubric is submitted
* Only force overview mode when not in query parameters
* Fix non-editable general feedback area
* Make sure non top-level submenus are hidden

Version 0.23.13 (GodfriedMetDenBaard.1)
-----------------------------------------

**Released**: April 24th, 2018

Fixes
^^^^^^^^^^^^^^^^^^^^

* Actually make sure permissions are not deleted in migration
* Make sure data is reloaded when switching course
* Store submissions filter on any keyup, not just enter
* Fix points width in non-editable rubric editor
* Fix width of rubric items after 4th one
* Fix (some of) the mess that is the rubric viewer
* Fix tab borders in the dark theme
* Use placeholder for the "new category" field in the rubric editor
* Make sure general comment is updated after switching submission

Version 0.23.5 (GodfriedMetDenBaard)
--------------------------------------

**Released**: April 24th, 2018

Features
^^^^^^^^^^^^^^^^^^^^

* Update readme and add new sections to it
* Add linters feature
* Add fixed max points feature
* Use pylint instead of pyflake for linting
* Make `pytest` run with multiple threads locally
* Revamp entire frontend design
* Make sure docs are published at docs.codegra.de

Fixes
^^^^^^^^^^^^^^^^^^^^

* Make sure upload dialog is visible after deadline
* Fix assignment state component
* Make sure no persisted storage is used if it is not available
* Fix the submission navbar navigation
* Rename `stupid` to `student` in test data
* Reduce the default permissions for the `TA` role
* Fix bug with changing language after changing file
* Fix thread safety problems caused by global objects
* Fix problems with ignoring directories
* Fix race condition in grade passback
* Fix not catching errors caused by invalid files
* Fix error when submitting for an LTI assignment without sourcedid

Packages Updates
^^^^^^^^^^^^^^^^^^^^

* Upgrade NPM packages

Version 0.22.1 (FlipFloppedWhiteSocked.2)
-------------------------------------------

**Released**: February 17th, 2018

Fixes
^^^^^^^^^^^^^^^^^^^^

* Make sure upload dialog is visible after deadline

Version 0.21.5 (FlipFloppedWhiteSocked.1)
-----------------------------------------

**Released**: January 25th, 2018

Fixes
^^^^^^^^^^^^^^^^^^^^

* Fix assignment state buttons for LTI assignment


Version 0.21.4 (FlipFloppedWhiteSocked)
----------------------------------------

**Released**: January 24th, 2018

Features
^^^^^^^^^^^^^^^^^^^^

* Make it possible to force reset of email when using LTI
* Add done grading notification email
* Make the way dividing and assigning works more intuitive
* Email graders when their status is reset to not done
* Add registration page
* Split can manage course permission
* Add autocomplete for adding students to a course
* Add the first implementation of TA communication tools
* Add the :kbd:`Ctrl+Enter` keybinding on the .cg-ignore field
* Make it possible to reset password even if old password was NULL.
* Add permission descriptions

Fixes
^^^^^^^^^^^^^^^^^^^^

* Fix the reload behaviour of snippets
* Make sure very large rubrics do not overflow the interface
* Increase the speed of multiple routes and pages
* Make sure the deadline object is cloned before modification
* Make sure existing users are added to course during BB-zip upload
* Make sure assignment title is only updated after submitting
* Make sure a zip archive always contains a top level directory
* Make sure a grade is always between 0 and 10
* Normalise API output
* Communicate better that certain elements are clickable
* Fix: "Files can be deleted even when they have comments associated with them"
* Make sure grades are compared numerically if this is possible
* Make blackboard zip regex handle more edge cases

Version 0.16.9 (ExportHell)
----------------------------

**Released**: November 23rd, 2017

Features
^^^^^^^^^^^^^^^^^^^^

* Make it possible to give feedback without any grade
* Make it possible to export username and user-id in csv
* Add utils.formatGrade function to format grades with 2 decimals
* Teacher revision interface
* Add cgignore file
* Add weight fields to submission divider
* Courses actions buttons *nicefied*

Fixes
^^^^^^^^^^^^^^^^^^^^

* Fix `null` in submission navbar
* Fix various bugs with boolean parsing for sorting
* Fix reset button on user info page
* Make sure selected language is reseted if file is changed
* Fix filter and order in submission navbar
* Make sure ordering grades will work as expected
* Fix makefile's phony targets
* Make sure that the default config uses the application factory
* Fix concurrent grade passback
* Define media queries in the mixins file
* Make sure comments or linters do not stop submission deletion
* Redo LTI launch if it fails because of a 401 error
* Put course list popovers above buttons instead of at the sides
* Fix rubric-points colour in the dark theme when overridden
* Make sure submissions can be deleted even if there is a grade history
* Make sure sorting tables works as expected
* Make sure blackboard zips with multiple files are uploaded correctly

Version 0.12.6 (DobbeleJava)
----------------------------

**Released**: September 21st, 2017

Features
^^^^^^^^^^^^^^^^^^^^

* Add a dark theme to the website.
* Revamping exporting all submissions by making it possible to include feedback and fixed a bug that prevented the name of the grader to show.

Fixes
^^^^^^^^^^^^^^^^^^^^

* Fix bug that prevented downloading code of persons non `latin-1` characters in their names.
* Fix behaviour of next and previous buttons in the code viewer.
* Fix handling of long lines in the code viewer.
* Fix bug where a lot of grader change requests were done when changing filters on the submissions page.
* Fix html injection bugs.
* Make it possible to click on the login button again.
* Make sure underlines in the code viewer are only done on code, not on the feedback.
* Fix bootstrap Vue input fields not showing text.
* Fix bug that resulted in a large white space between the header and the body in LTI when dark mode is enabled.
* Fix bug that file tree viewer was way too long overlapping the footer.
* Fix bug that resulted in that every grade attempt showed as a new submission in the LMS.
* Fix bug that some floating point rubric items points resulted in very large descriptions overlapping the grade viewer.

Version 0.10.0 (Columbus)
--------------------------

**Released**: September 12th, 2017

Features
^^^^^^^^^^^^^^^^^^^^

* Make it possible for a user to reset its password
* Allow to change font size and store it in vuex
* Add a whitespace toggle button and language dropdown to the code viewer
* Make it possible to disable incremental rubric submission
* Add new course and assignment
* Add global permission managing system

Fixes
^^^^^^^^^^^^^^^^^^^^

* Fix jumping text when toggling directories in the file tree
* Fix unicode errors while creating files.
* Make rubric deletion also not save directly when incremental rubric submission is off
* Fix various filesystem api bugs
* Fix file-links in the code viewer
* Fix undefined error on submission page
* Fix a bug where files would be left open after submitting archive
* Remove item description popover
* Make sure global permissions are checked in the front- and back-end
* Fix issue where error would disappear immediately after submitting with the keyboard

Packages Updates:
^^^^^^^^^^^^^^^^^^^^

* Upgrade bootstrap-vue

Version 0.3.2 (Belhamel)
-------------------------

**Released**: September 4th, 2017

Features
^^^^^^^^^^^^^^^^^^^^

* Add delete submission feature
* Add privacy notes
* Update rubric selector and creator front end
* Make it possible to upload files by dragging and dropping
* Make it possible to disable automatic LTI role creation
* Add codecov as coverage reporter
* Change submission assignee from submissions list
* Add documentation for how to run CodeGra.de
* Add grade history
* Sort rubric items in the rubric viewer
* Improve site navigation
* Make it possible to delete a grade
* Make it possible to submit non integer grades
* Autofocus username field on login page
* Allow to update name and deadline of an assignment separately
* Make it possible again to grade work
* Make duplicate emails possible

Fixes
^^^^^^^^^^^^^^^^^^^^

* Fix all missing or wrong quickrefs on api calls
* Fix stat api route
* Fix graders list of an assignment being loaded without correct permissions
* Fix bug where only the second LTI launch would work
* Fix front-end feature usage
* Clear vuex cache on :kbd:`Ctrl+F5`
* Fix timezone issues on a LTI launch with deadline info
* Make sure all test files are directories
* Fix course link on assignment page
* Fix downloading files from server
* Fix unknown LTI roles
* Fix undefined issues in LTI environments
* Add test-generated files to gitignore
* Fix seed_data and test_data paths
* Create update api
* Rewrite submission page
* Fix bugs introduced by postgres
* Add links to them fine shields

Package Updates
^^^^^^^^^^^^^^^^^^^^

* Remove pdfobject and pdf.js dependencies
* Move bootstrap-vue dependency to own org
* Add npm-shrinkwrap.json and delete yarn.lock
* Change to JWT tokens

Version 0.2.0 (Alfa)
---------------------

**Released**: July 21st, 2017

Initial CodeGrade release
