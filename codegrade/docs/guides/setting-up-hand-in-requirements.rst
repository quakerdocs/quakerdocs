.. _guide_hand_in_requirements:

Set up hand-in requirements for a CodeGrade assignment
=======================================================

.. deprecation_note:: /for-teachers/configuring-your-assignment/setting-up-hand-in-requirements

It is desirable to have strict hand-in requirements and instructions for some
programming assignments. Perhaps to make manual or automatic testing less
cumbersome or to disallow the handing in of certain unwanted files.

CodeGrade offers an elaborate means to set up hand-in requirements for
assignments that *force* students to hand in files or archives with a requested
structure. Follow the guide below to learn how to set this up for your CodeGrade
assignment:

1. Go to the **Assignment Management** page for the assignment you want to add hand-in requirements to by clicking on the :fa:`cog` button.

2. Under the **General** tab, locate the **Hand-in requirements** section. You
   can choose to copy the instructions over from another assignment, or set up
   a new requirements schema.

3. Select the policy of your requirement:

    - **By default** *Deny all files*: All files are denied by default, further rules (*required* or *allowed files*) determine exactly and strictly what students can or must hand in (i.e. this will allow you to whitelist certain files and deny anything else).
    - **By default** *Allow all files*: All files are allowed by default, further rules (*required* or *denied files*) determine which specific files a student cannot hand in or must hand in (i.e. this will allow you to blacklist certain files and allow anything else).

4. After selecting either of the policies above, more options are displayed to further specify the behaviour of your requirements:

    - **Delete empty directories**: If enabled, automatically delete empty directories in submissions.
    - **Delete leading directories**: If enabled, automatically delete superfluous leading directories (i.e. top-level directories in which all files / subdirectories are located).
    - **Allow overrides by students**: If enabled, the student can, after being shown a warning, still force hand in the submission even if it violates the hand-in requirements.

5. Subsequently, rules to make exceptions for the set policy can be given in the **Exceptions and requirements** section. The following rules can be created:

    - **Required**: This rule is available to both default policies and can be used to require students to hand in certain files.
    - **Allowed**: This rule is available if all files are *denied* by default and can be used to make exceptions to this policy. Files and folders indicated as allowed are allowed to be handed in.
    - **Denied**: This rule is available if all files are *allowed* by default and can be used to make exceptions to this policy. Files and folders indicated as denied cannot be handed in.

.. warning::

    The exceptions and requirements are individual rules that act as exceptions
    to the chosen policy. There is no ordering between rules.

.. note::

    Use ``/`` or ``\`` as a directory separator to specify that certain files are
    required, allowed or denied in a directory. Start the rule with a directory
    separator (``/`` or ``\``) to specify that a file is required, allowed or denied in
    the top level directory.

    To match more than one file, you can use a single wildcard for the name of
    the file, by using a ``*``. For example ``/src/*.py`` matches any file ending with
    ``.py`` in the directory src that is directly in the top level directory of the
    submission.

6. When the default policy, options and exceptions and requirement rules are set up to your wishes, press the **Submit** button to save the hand-in requirements.

Once hand-in requirements are set up for an assignment in CodeGrade, students
are provided with the **Hand-in instructions** tab on the assignment upload page
with an overview of the set up instructions and requirements.

Furthermore, if a student submits a submission that is not conform the
requirements, a warning will be shown. Unwanted files will automatically be
detected and deleted.
