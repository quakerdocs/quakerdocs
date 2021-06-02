Overview of CodeGrade
======================

.. deprecation_note:: /for-teachers/getting-started

CodeGrade can be used both as a stand-alone web application and as a module in
your LMS. The following chapters apply to both situations. Please consult the
:ref:`LMS Integration <lms-chapter>` chapter for detailed information of
integrating CodeGrade with your Learning Management System.

This chapter provides a brief overview of the components and navigation in
CodeGrade.

.. note::

    CodeGrade uses an extensive :ref:`permissions <permissions-chapter>` system
    that may allow certain features to be disabled on your CodeGrade account.

General Site
-------------

CodeGrade allows for the :ref:`creation of courses and assignments
<management-chapter>`.

.. note:: CodeGrade assignments can also be created in co-operative Learning
   Management Systems.

Each assignment is part of a course and each course can have multiple
assignments linked to it. All courses and assignments have individual settings
pages. With the right :ref:`permissions <permissions-chapter>` these pages allow
for adding users to the course, changing the details of an assignment, dividing
submissions over teachers, setting up automatic testing, setting hand-in
requirements, sending notifications to students and teachers and adding or
customizing rubrics.

Assignments handed in via CodeGrade can be viewed using the :ref:`Codeviewer
<codeviewer-chapter>`. The Codeviewer allows for a convenient way to review and
grade submissions online. The features include line for line feedback and a file
browser.

New courses can be created by the site administrators. They can also add
students, teachers and teaching assistants to these courses. New roles can be
created and :ref:`permissions <permissions-chapter>` of existing roles can be
altered by site administrators too. All users on CodeGrade can set
:ref:`personal site preferences and edit account information
<preferences-chapter>`.

Filesystem
-----------

The `CodeGrade Filesystem <https://fs-docs.codegra.de>`__ (or CodeGra.fs) can be
used in combination with the web application.  It can mount a local CodeGrade
instance on your computer to browse the assignments and files on the server. The
filesystem can be used for students to locally work on the CodeGrade mount and
thus automatically hand in the assignment with each save.  For teachers the
filesystem can be used to locally grade work without any overhead using a
preferred editor.

All features of the online :ref:`Codeviewer <codeviewer-chapter>` (e.g. line for
line feedback, filling in rubrics and adding general grades and feedback) can
also be done locally using the filesystem. Editor plugins can be installed and
used for most popular editors to enable this.

Account Management
-------------------

Creating a new account
~~~~~~~~~~~~~~~~~~~~~~~
You must have a CodeGrade account in order to use CodeGrade and follow courses.
If your CodeGrade instance is linked with a Learning Management System (LMS)
a new account will automatically be registered when you visit your first
CodeGrade assignment in your LMS.

Otherwise you can create an account by navigating to your institute's CodeGrade
site (e.g. uva.codegra.de) and clicking the 'Register' button. Here you can
register a new account by entering your full name, a valid email address and
a password. Also a unique username has to be chosen to finish registration,
please keep in mind that this username cannot be changed after your
registration is complete.

You are now registered and logged in to CodeGrade!

.. note:: Registering a new account in this way may not be available on your
   CodeGrade instance.

Logging in to an existing account
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are multiple ways to log in to CodeGrade. If you visit CodeGrade via your
Learning Management System (Blackboard, Canvas, etc.) you do not need to enter
any password as you will automatically be logged in. If you are on a standalone
CodeGrade instance, you can log in either with a username and password
combination or via a single sign-on (SSO) provider.

To log in with your username and password, you need to already have registered
an account. Visit <instance>.codegra.de, click 'Login' in the sidebar, and
enter your username and password. After clicking the 'Login' button you are now
logged in to CodeGrade!

To log in with SSO select your institution in the list of SSO providers. You
will be taken to a page where you can log in to the SSO system, which will take
you back to CodeGrade afterwards. When you return you will be logged in to
CodeGrade.

Click 'Forgot password' in the case you have forgotten your password. After
entering your username, a temporary link will be sent in an email which allows
you to reset your password. Please consult your institute in the case of
a forgotten username or an incorrect email address.

.. note:: Please check your spam filter if no email is received shortly after
   the request.
