.. _lms-chapter:

LMS Integration
=================

.. deprecation_note:: /

CodeGrade works together with learning management systems (LMS) with the
*Learning Tools Interoperability* (LTI) standard. This chapter explains
integrating CodeGrade into your LMS and CodeGrade's behaviour when working
together with your LMS.

For exact details on how to add CodeGrade as an external tool in your LMS, which
should be done by the system administrator of the LMS, please
:ref:`contact us<contact-chapter>`.

Blackboard
------------
CodeGrade integrates with the `Blackboard Learn
<https://www.blackboard.com/blackboard-learn/index.html>`__ learning management
system through LTI. New CodeGrade assignments can then be created from within
Blackboard.

To create a CodeGrade assignment in Blackboard, go to a course's *Content* page
and select *CodeGrade* from the *Build Content* menu.

.. warning::

    For the new assignment, do **not** turn off the *Enable Evaluation*
    option, and make sure that *Points Possible* is set to a number greater
    than 0, otherwise grades will not appear in Blackboard's grade center.

    Also, do **not** set a deadline for the assignment in Blackboard.
    Blackboard will mark all submissions *late*. Instead, immediately after
    creation of the new assignment, visit the assignment in CodeGrade and
    set the deadline there.

.. note::

    When CodeGrade is connected to Blackboard, all assignments should be
    graded on a scale from 0 to 10 in CodeGrade. When the maximum points
    that can be achieved should be something other than 10, the *Points
    Possible* option can be set in Blackboard for the assignment.
    Blackboard will then scale the grade it received from CodeGrade
    linearly to this value.

Brightspace
-----------
CodeGrade integrates with the `Brightspace <https://www.brightspace.com/>`__
Learning management system through LTI. New CodeGrade assignments can then
be created from within Brightspace.

.. warning::

    Setting a deadline, or other visibility rules in Brightspace, are **not**
    synchronized with CodeGrade. You should set a deadline in CodeGrade after
    creating an assignment, as otherwise students will not be able to submit
    their work.

Canvas
--------
CodeGrade works together with the popular open-source learning management system
`Canvas <https://www.canvaslms.com/>`__ through LTI. By integrating CodeGrade as
an external app in Canvas, CodeGrade assignments can be created.

It is now possible to create CodeGrade assignments in your Canvas course.
Choose the *External Tool* option as *Submission Type* and select CodeGrade
in the *Find* menu.

.. note::

    We recommend grading assignments in CodeGrade's stand-alone environment so
    more *screen-space* is used for grading. Your are automatically logged in
    to this environment with a linked CodeGrade account after opening CodeGrade
    through Canvas.

Moodle
--------
CodeGrade integrates with the `Moodle <https://moodle.org/>`__ learning management
system through LTI. New CodeGrade assignments can then be created from within
Moodle.

.. warning::

    Setting a deadline, or other visibility rules in Moodle, do **not** sync to
    CodeGrade. You should set a deadline in CodeGrade after creating an
    assignment, as otherwise students will not be able to submit their work.

.. note::

    When CodeGrade is connected to Moodle, all assignments should be
    graded on a scale from 0 to 10 in CodeGrade. Scaling, and maximum points can
    be set in Moodle.

Sakai
-----
CodeGrade integrates with the `Sakai <https://sakailms.org/>`__ learning management
system through LTI. New CodeGrade assignments can be created from within Sakai.

.. warning::

    Setting a deadline, or other visibility rules in Sakai, do **not** sync to
    CodeGrade. You should set a deadline in CodeGrade after creating an
    assignment, as otherwise students will not be able to submit their work.

Other LMS
-----------
CodeGrade is currently working on adding support for more learning management
systems too. Please :ref:`contact us <contact-chapter>` for more information
about support of your learning management system.

CodeGrade LMS Behaviour
-------------------------
CodeGrade works together with the learning management system through LTI to
synchronise i.a. users, courses, assignments and grades. The following behaviour
is specified:

.. _lms-create-course-or-assig:

Creating Courses or Assignments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Course and assignment creation is done using your learning management
system environment. A corresponding CodeGrade course will automatically be
created When creating a CodeGrade assignment in your LMS. Management of your
assignment is mainly done in CodeGrade. The assignment name and deadline,
however, are managed in your LMS, and optionally the state (e.g. *published*
or *unpublished*) if your LMS supports it.

.. note::

    Assignment and course names do not have to be unique.

.. note::

    The LMS assignment states *unpublished* and *published* correspond with
    CodeGrade's *hidden* and *open* states, respectively. CodeGrade's *done*
    state does not correspond with any LMS state and does not automatically
    change with LMS assignment management.

Users are not added to the CodeGrade course right away, however only added to
CodeGrade after opening the CodeGrade assignment in the LMS.
Users' roles are automatically saved from the LMS to CodeGrade when creating an
assignment, however these can be changed inside CodeGrade later on.

.. _lms-grading:

Grading
~~~~~~~~
When grading in CodeGrade is done, grades can be *passed back* to the LMS by
manually setting the assignment state to *done* in CodeGrade (see
:ref:`Assignment States <manage-assignment-state>`). Grades saved when the
assignment state already is *done* are automatically passed back to the LMS.

.. warning::

    Grades are **not** automatically passed back to the LMS but require the
    CodeGrade assignment state to be set to *done*.

Setting the CodeGrade assignment state back to *not done* will not automatically
hide grades in your LMS, but only hide the grades in CodeGrade. Setting the
assignment to muted in your LMS will also not hide the grades in CodeGrade if
the assignment state is *done*. This is because of the fact that
CodeGrade's *done* state does not correspond with any LMS state and does not
automatically change with LMS assignment management yet.

.. _lms-account-linking:

Account Linking
~~~~~~~~~~~~~~~~~
Accounts in your LMS are automatically linked or synchronised to CodeGrade
accounts. Opening a CodeGrade assignment in your LMS will automatically log you
in to CodeGrade with a CodeGrade account that is linked to your LMS account.
CodeGrade has specified behaviour for multiple cases:

* A new CodeGrade account will be created and linked to your LMS account if you
  open a CodeGrade assignment in your LMS and no existing CodeGrade account is
  linked yet.
* Your current CodeGrade account will be linked to your LMS account if you are
  logged in to CodeGrade and open a CodeGrade assignment in your LMS and your
  current CodeGrade account is not yet linked.
* You will automatically log in to the CodeGrade account linked to your LMS
  account if you open a CodeGrade assignment in your LMS and you are currently
  not logged in to CodeGrade.
* You will switch CodeGrade accounts if you are currently logged in to
  a CodeGrade account but *another* CodeGrade account is linked to your LMS
  account while opening a CodeGrade assignment in your LMS.
