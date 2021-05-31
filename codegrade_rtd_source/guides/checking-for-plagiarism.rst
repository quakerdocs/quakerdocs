.. _checking-for-plagiarism:

Check for plagiarism in a CodeGrade assignment
======================================================

.. deprecation_note:: /user-reference/assignments/plagiarism

CodeGrade has integrated state of the art plagiarism software powered by JPlag
to find possible plagiarism cases in CodeGrade assignments. This guide will walk
you through setting up a plagiarism run.

1. Go to the **Assignment Management** page for the assignment you want to do plagiarism detection on by clicking on the :fa:`cog` button.

2. On the **Assignment Management** page, navigate to the **Plagiarism** tab. This is where plagiarism checks can be run and where previous plagiarism checks can be reviewed.

3. Set up the options to apply to your assignment:

    - **Language**: Language of the code in the assignment.

    .. note::

        Please contact us if your required language is not present in this list.

    - **Suffixes to include:** Comma separated list of suffixes of files to include in the check. Leave empty to use the default suffixes for the selected language.
    - **Minimal similarity:** The minimal average similarity to include in the results, the default is an average of 25%.
    - **Old assignments:** Optionally one or more previous CodeGrade assignments can be selected, so that submissions from these assignments are included in the plagiarism check.
    - **Old submissions:** Optionally an archive with assignments or codebase can be uploaded to be included in the plagiarism check.
    - **Base code:** Optionally an archive with code to be excluded in the plagiarism check can be uploaded to reduce false positives. Use this to upload e.g. a framework used by all students.

4. Click the **Run** button to start the plagiarism check. A new entry will be created above the option fields and will display the progress.

5. When the plagiarism check finished, press the plagiarism run entry to display an overview of detected plagiarism cases.

6. The following **Plagiarism Overview** page displays an overview of all plagiarism cases between students (or optionally between supplied old code). Click on any row to investigate the specific case.

7. The **Plagiarism Comparison** shows two code views with the files that contain potential plagiarism, the actual individual plagiarism cases are highlighted with a colour corresponding to the colours in the top menu. Press these to compare manually.

.. note::

    Click the **Export** button on the top right hand corner to export
    a plagiarism report. Plagiarism cases can be exported in Docx or LaTeX
    format, so that additions and further comments can be added before
    exporting as PDF.
