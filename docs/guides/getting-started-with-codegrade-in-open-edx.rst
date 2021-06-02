Getting started with CodeGrade in Open edX
-----------------------------------------------

.. include:: getting-started-introduction.rst

Integration with Open edX
=============================

All functionalities are bundled in one complete environment for programming
education, that integrates with Open edX. We use the LTI protocol to securely
communicate and synchronise CodeGrade with Open edX. Most likely, CodeGrade has
already been correctly integrated with Open edX by your system administrator,
please contact us if not.

CodeGrade accounts are automatically created and linked to current Open edX
accounts. CodeGrade can be accessed both from **within Open edX**, showing a
more narrow version of CodeGrade in a container on Open edX, or from the
CodeGrade **standalone website**: *<your-institution>.codegra.de*. There is no
difference between these two, and opening the standalone website via Open edX
using the **“New tab”** button allows you to be automatically logged in.

CodeGrade accounts that are automatically created and linked from within Open
edX will not have a password, and are only accessible by the shared session with
Open edX.

.. include:: setup-password.rst

Open edX synchronisation
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following data is shared between CodeGrade and Open edX:

- Usernames

- Full names

- Email addresses

- Course names

- Assignment names

- Assignment state

- Grades (only passed back from CodeGrade to Open edX)

Setting up your course
========================

After creating your first CodeGrade assignment from within Open edX, a course
will be automatically created in CodeGrade. To **manage** the course options
**press “Courses”** (:fa:`book`), select your course and press the :fa:`cog`
**icon**. Below is a brief overview of the tabs in course management.

Members
~~~~~~~~

After a user (student, TA or teacher) opens a CodeGrade assignment in Open edX
for the first time in your course, they will automatically be added as a member
of the course, CodeGrade will use the **role** this user has in Open edX.  On
this tab, you can **change the role** of a member if it’s not correct, for
example, from **Student** to **TA**.

.. warning::
    CodeGrade will automatically use the role the user has in Open edX. In
    general, it is not necessary to change roles, only do this if necessary.

Permissions
~~~~~~~~~~~~

On this page, you can change the permissions of the roles in the course. For
example, you could give your TAs more permissions. Every permission is explained
by the :fa:`info` icon.

.. warning::
    The default permissions will probably suit your course.

Groups
~~~~~~~~~

If you want to use groups, you can create group sets here. A group set can be
used by multiple assignments in the same course. **CodeGrade does not
synchronise groups with Open edX**, so make sure your assignments in Open edX
are individual assignments (no group submission) and manage your groups in
CodeGrade. **CodeGrade will automatically send back all grades and feedback to
all individual group members to Open edX correctly.**

Depending on permissions you can allow students to join a group themselves or
only allow Teachers or TAs to add students to a group. If you want to
**change** these permissions, you can do so on the **permissions** page
explained above.  :ref:`Click here to learn more about setting up your groups
<set-up-group-assignment>`.

Setting up your assignment
=============================

By clicking the :fa:`cog` icon on an assignment you enter the **assignment
management page**. This page allows you to set up **groups**, start
**plagiarism runs**, add or edit the **rubric**, and set up **automatic
testing**.

General
~~~~~~~~~

On the **“General”** page you can edit several general options. You can also select
a group set to use, if you decide to make an assignment a group assignment.
Furthermore you can set bonus points.

.. warning::

    Manage the **deadline** of the assignment in CodeGrade and **NOT** in Open edX.

.. warning::

    The name and points possible of the assignment are configured within Open edX.

.. include:: includes/getting-started-general.rst

Student Experience
=====================

Students hand in an assignment on **Open edX** via the CodeGrade container after
opening the assignment or optionally via Git. After handing in, students can
browse through their code to check if it is correctly handed in. Before handing
in they can click on the **“rubric”** (:fa:`th`) button to show the rubric for
this assignment.  This means students **know what is expected** of them.

After an assignment is set to **“Done”** (:fa:`check`) grades are automatically
sent back to Open edX. Students can then view their feedback inside the
CodeGrade container in Open edX after clicking on their grade or navigating to
the assignment.

.. note::

    If an assignment is in the **“Done”** (:fa:`check`) state, all new grades
    or edits are passed back to Open edX immediately.

After uploading, a student will find an overview of their **Code** (where they
can browse through their handed in files), an overview of their **Feedback**
and optionally an overview of the **AutoTest** results which can be filled in
preliminarily with Continuous Feedback.

.. note::

    We recommend graders to make use of the standalone CodeGrade website, but
    the CodeGrade container within Open edX is sufficient for students. It is
    not possible for students to hand in assignments in the standalone
    environment.

Contact us and support
========================
If you have any questions, don’t hesitate to contact us. You can email us at
`support@codegrade.com <mailto:support@codegrade.com>`_. In addition to
questions and bug reports, we always love to get feedback and suggestions on
how we can improve CodeGrade to better fit your education.
