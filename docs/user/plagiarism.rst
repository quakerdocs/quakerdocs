.. _plagiarism-chapter:

Plagiarism Detection
=====================

.. deprecation_note:: /user-reference/assignments/plagiarism

CodeGrade's code plagiarism detection feature can be found on the
:ref:`assignment management <management-chapter>` page. Here, new plagiarism
runs can be done and previous runs can be examined for plagiarism.

.. warning:: Individual plagiarism cases should always be manually reviewed.

Running the Plagiarism Checker
-------------------------------
As of writing, CodeGrade offers plagiarism detection using the
`JPlag <https://github.com/jplag/jplag>`__ code plagiarism detection tool.
Alternative plagiarism tools will be supported in the near future.

Multiple settings can be set when checking for plagiarism:

* The programming language has to be selected from a list of supported
  languages. If the required language is not present in the list, it is no
  problem to select a language with similar syntax and structure.
* Suffixes, separated by commas, of the files to include can be given. Set to
  ``.*`` to include files with all suffixes and leave empty to automatically
  select suffixes based on the chosen programming language.
* The minimal average similarity of a case to include in the results can be
  set. For JPlag this is a percentage: ``100`` means exactly the same and
  ``50`` means an average of 50%. This is default set to ``25``.
* Finally an old assignment can be selected to include in the plagiarism check.
  This can for instance be the same assignment from a previous year or course.
  Submissions from previous assignments are only used to check with current
  submissions and cases between two previous submissions are not included in
  the results.

Additionally, instead of selecting an old CodeGrade assignment to check against,
an archive with old submissions to check against can be uploaded.
This should be an archive whose top level entries are treated as a separate
submission. The top level entry can either be a directory or archive whose
contents count as a submission, or a single regular file which counts as the
entire submission.

Finally, an archive with *base code* can be uploaded. Code in this archive will
be excluded in the plagiarism check to reduce the amount of false positives.

.. note:: It is often a good practice to upload template code or provided code
   snippets as *base code* to be excluded.

JPlag Characteristics
~~~~~~~~~~~~~~~~~~~~~~

JPlag is an open source software plagiarism detection tool that is developed by
the Karlsruhe Institute of Technology, who describe JPlag as:

    JPlag is a system that finds similarities among multiple sets of source
    code files.  This way it can detect software plagiarism. JPlag does not
    merely compare bytes of text, but is aware of programming language syntax
    and program structure and hence is robust against many kinds of attempts to
    disguise similarities between plagiarized files.  JPlag currently supports
    Java, C#, C, C++, Scheme and natural language text.

    JPlag is typically used to detect and thus discourage the unallowed copying
    of student exercise programs in programming education. But in principle it
    can also be used to detect stolen software parts among large amounts of
    source text or modules that have been duplicated (and only slightly
    modified). JPlag has already played a part in several intellectual property
    cases where it has been successfully used by expert witnesses.

Taken from `JPlag <https://jplag.ipd.kit.edu/>`__, please consult for more
information.

Extend JPlag with CodeGrade
~~~~~~~~~~~~~~~~~~~~~~~~~~~

At CodeGrade we have extended JPlag to understand a lot more languages at the
request of our partners. Do you need support for a language that is not on the
list of supported languages? Send us an email at `support@codegrade.com
<mailto:support@codegrade.com>`__ and we'll see what we can do!

The languages we have added so far are:

- JavaScript
- JSON
- Jupyter notebooks
- PHP
- R
- Scala

Reviewing Plagiarism
---------------------
After the plagiarism checker is done running, its results can be found under the
*Previous Runs* tab. The run can be deleted by pressing the :fa:`times` button
or reviewed by clicking on the entry itself to find an overview page with all
the potential plagiarism cases.

This overview page displays potential plagiarism cases between students, with
the maximum score and the average score. The cases can be filtered on student
name by using the filter bar on top.

More details can be found by clicking on the individual cases. The individual
plagiarism comparison page displays the specific correspondences found between
the submissions of the students. These individual correspondences are coloured
differently, clicking a correspondence will display the correspondence in
the code. This page can be used to review the individual plagiarism cases.

.. note:: Use the plagiarism button in the sidebar to quickly toggle between plagiarism cases when reviewing individual cases.

Exporting Plagiarism Cases
~~~~~~~~~~~~~~~~~~~~~~~~~~~
A report for an individual potential plagiarism case can be exported from the
individual plagiarism comparison page. Either a `LaTeX
<https://www.latex-project.org/>`__ ``.tex`` or a `Docx
<https://docs.microsoft.com/en-us/openspecs/office_standards/ms-docx/b839fe1f-e1ca-4fa6-8c26-5954d0abbccd>`__
file that includes the code segments and can be supplemented with additional
comments can be exported.

Select the plagiarism correspondences to be included in the report and press the
*Export* button to generate the `.tex` file.

Optionally, select the *Each listing on a separate page* option under **Options**
to have each listing (i.e. printed code segment) on a new page.

.. note:: Make sure pop-ups from CodeGrade are allowed in your browser if downloading fails.
