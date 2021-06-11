.. _permissions-chapter:

Permissions
=============

.. deprecation_note:: /user-reference/courses-general/permissions

CodeGrade works with an extensive permission system to allow different types of
users (*roles*) to access and manage things on the site.

The permissions are divided into site-wide permissions and course
permissions. Site-wide permissions are administered by the site administrators
and apply to all courses. Course permissions only apply to one course and
CodeGrade users can have different roles and permissions for different courses.

.. _site-permissions:

Site Permissions
------------------
General site permissions can be accessed by the :fa:`tachometer` button, which
is only visible to site administrators. Four roles are provided for site
permissions: admin, staff, student and nobody (no role).

The available global permissions can be found in the
`table below <GlobalPermissions_>`_.

.. csv-table:: Global permissions
   :file: ../global_permissions.csv
   :name: GlobalPermissions
   :widths: 20, 70
   :header-rows: 1

.. _course-permissions:

Course Permissions
-------------------

Permissions and roles can be specified per course, this can be done in
:ref:`course management <course-management>` under the *roles* tab. The five
default roles are: designer, observer, student, TA (teaching assistant) and
teacher. Default roles can be removed, their permissions can be altered and new
roles can be added to the course.

The available course permissions can be found in the
:ref:`table below <CoursePermissions>`.

.. note::

  Roles can only be removed if no current users act in that role in the course.

.. example:: allow late submissions by creating a new role

  To temporarily allow late submissions by some students, you can create a *Late
  Student* role with the permission "Upload after deadline". Now if you want to
  allow late submissions by a student, you can change the role of this student
  to *Late Student*.

.. csv-table:: Course permissions
   :file: ../course_permissions.csv
   :name: CoursePermissions
   :widths: 20, 70
   :header-rows: 1

.. note:: Permissions indicated with `*` are added by default for new roles.
