.. _analytics-dashboard:

Analytics Dashboard
===================

.. deprecation_note:: /user-reference/analytics-dashboard

CodeGrade's Analytics Dashboard is built to give you insight in both how
students are doing on an assignment, as well as where an assignment can be
improved to optimize the learning process. You can create selections of all the
submissions for an assignment using filters. These selections are displayed in
parallel in intuitive graphs. There are graphs for when and how many times
students submitted their work, the distribution of grades, and, if the
assignment has a rubric, statistics about the rubric's categories.

.. _analytics-dashboard-general-statistics:

General statistics
------------------

The general statistics show statistics over all submissions and are not subject
to the selected filters.

- **Students** or **Groups**: the total number of students (or groups if this
  is a group assignment) that submitted their work.
- **Submissions**: the total amount of submissions for this assignment.
- **Average grade**: the average grade over the latest submissions of each
  student. The latest submission is used here because that is the grade that
  a student will get for this assignment.
- **Average submissions**: the average amount of submissions per student.

The :fa:`info` information popovers list some other useful statistics about the
grade:

- **Mean**: the mean value of the sample.
- **Std. deviation**: the sample standard deviation from the mean.
- **Median**: the median value of the sample. This is the middle value in the
  sorted list of values.
- **Mode**: the mode of the sample. This is the most common value in the
  sample.

.. note::
    Since these statistics do not necessarily follow the normal distribution it
    is not always the case that ~66% of students lie within 1 standard
    deviation from the mean.

Filters
-------

Filters can be used to select a subset of the available data. You can create
multiple filters to select multiple datasets that will be visualized in
parallel. Each dataset will have its own distinct color in the charts in the
rest of the page. The default filter selects the latest submission of each
student.

.. note::
    It is possible to create overlapping datasets, e.g. two datasets that
    contain the same submission. This leads to a bias in your data, making it
    very difficult to take fair conclusions.

.. note::
    When an assignment does not have many submissions to begin with, applying
    filters will decrease the size even further. Make sure that the amount of
    submissions per selection is sufficient to take any conclusion.

Filter options
~~~~~~~~~~~~~~

Each filter has a set of options that narrow the scope of its selection.

- **Latest**: when checked, only the latest submission by each student is
  selected. Otherwise all submissions of each student are used.
- **Min. grade**: only select submissions with a grade equal to or greater than
  this number.
- **Max. grade**: only select submissions with a grade strictly less than this
  number.
- **Submitted after**: only select submissions from this date or after.
- **Submitted before**: only select submissions from strictly before this date.
- **Graders**: only select submissions assigned to one of the selected graders.

At the bottom of each filter there is a field showing the :ref:`general statistics
<analytics-dashboard-general-statistics>` for the submissions selected by this
filter.

Creating new filters
~~~~~~~~~~~~~~~~~~~~

There are multiple ways to create a new filter: click :fa:`plus` to add a new
default filter, click :fa:`copy` to duplicate an existing filter, or click
:fa:`scissors` to :ref:`split a filter
<analytics-dashboard-splitting-filters>`.

.. _analytics-dashboard-splitting-filters:

Splitting filters
~~~~~~~~~~~~~~~~~

You can split the set of submissions selected by a filter into several subsets.
Click the :fa:`scissors` button to start splitting a filter.

You are presented with a list of options how you want the set to be split up.
With the exception of the **Latest** option, the submissions are split into
several disjoint subsets.

- **Latest**: creates two sets of submissions. One will only contain the latest
  submission by each student, while the other has all submissions per student,
  including their latest submission.
- **Grade**: creates two disjoint subsets. One will contain only those
  submissions with a grade strictly lower than the entered value. The other
  will contain the rest of the submissions.
- **Submitted on**: creates two disjoint subsets, one containing all submissions
  that were submitted before the given date, and the other everything that was
  submitted after this date.
- **Grader**: creates a new subset for each selected grader. The subset per
  grader will only contain submissions that are assigned to that grader.

Below the splitting options is a field with :ref:`general statistics
<analytics-dashboard-general-statistics>` for each result that would be
produced by these splits.

Multiple splits can be applied at the same time. The resulting amount of
datasets will be the product of applying each separately.

.. warning::
    Splitting on multiple criteria makes the number of resulting filters grow
    exponentially in the number of criteria, and making a proper analysis
    quickly becomes unwieldy.

**Sharing filters**

You can click :fa:`share-alt` and then :fa:`clipboard` to share your current set of
filters with others.

.. note::
    Without the permission "Can view analytics" the Analytics Dashboard cannot
    be displayed.

Submission statistics
---------------------

The submission statistics consist of two diagrams.

The first is a histogram that shows, per interval of time, when students have
submitted their work. You can configure the range of dates that should be
visualised, and select a proper bin size.

The second histogram gives insight in how many submissions students have made.
The X-axis lists the amount of submimssions, and the Y-axis lists the number of
students that fall into that category.

Grade statistics
----------------

The grade statistics shows the distribution of grades. On the X-axis is the
grade and on the Y-axis the number of students that achieved that grade.

Rubric statistics
-----------------

The rubric statistics contains several diagrams giving insight in how students
scored on the rubric of this assignment:

- **Mean (default)** shows the mean score that students achieved per rubric
  category. The error bars indicate the standard deviation from the mean.
- **Median** is the median score per rubric category. The median is obtained by
  taking the middle value in the sorted list of scores.
- **Mode** gives the mode per rubric category. The mode is obtained by taking
  the most common value amongst a sample.
- **RIT** is the correlation, commonly denoted **R**, between the **I**\ tem
  and the **T**\ otal score.  :ref:`More details
  <analytics-dashboard-rit-rir>`.
- **RIR** is the correlation **R** between the **I**\ tem and the **R**\ educed
  score, where the rest score is the total score for the rubric minus the score
  for this category. :ref:`More details <analytics-dashboard-rit-rir>`.
- A **Correlation** diagram per rubric category plots the achieved scores in
  the rubric category against the :ref:`reduced score
  <analytics-dashboard-reduced-rubric-score>` of the entire rubric. Each point
  in the graph represents a single student. :ref:`More details
  <analytics-dashboard-correlation-diagrams>`.

.. _analytics-dashboard-reduced-rubric-score:

Reduced rubric score
~~~~~~~~~~~~~~~~~~~~

The reduced rubric score of a rubric category is the total amount of points
achieved for a rubric minus the amount of points achieved for the rubric
category. For example, if a student achieved 10 points in a rubric, of which
2 in the first rubric category, then their reduced rubric score for the first
rubric category is 8.

.. _analytics-dashboard-rit-rir:

The RIT & RIR values
~~~~~~~~~~~~~~~~~~~~

The **RIT** and **RIR** values of a rubric category are the correlation
coefficients between the score achieved in one rubric category category versus
how well they did in the overall rubric. Their value is a number between -1 and
1 measuring how well the score in a rubric category predicts the score in the
overall rubric.

Positive values indicate that students who scored higher in a rubric category
also scored higher in the entire rubric, while negative values indicate the
reverse: students who scored higher in this rubric category scored lower on the
overall rubric.

A negative value for a rubric category is an indication that something may be
off with the category and that it may need to be revised. It is not necessarily
the case, of course, so it is left to the discretion of the teacher to act upon
this.

While the RIT and RIR values are very similar, there is a subtle difference in
how they are calculated. The RIT value is calculated against the total score on
the rubric, but since this total score also includes the score for the
compared-to category the data is biased, because higher item scores
automatically lead to higher total scores. The RIR value overcomes this by
using the reduced rubric score instead of the total rubric score. Subtracting
the total score from the item score first, and only then calculating the
correlation between the two removes this bias. The RIR value is often a fairer
representation of the quality of a rubric category.

.. _analytics-dashboard-correlation-diagrams:

Correlation diagrams
~~~~~~~~~~~~~~~~~~~~

The correlation diagram of a rubric category has the achieved score in the
category on the X-axis versus the :ref:`reduced rubric score
<analytics-dashboard-reduced-rubric-score>` on the Y-axis. Each point in the
diagram represents a single student. These diagrams are useful to understand
where the RIR values of the rubric categories came from.

A linear line is drawn through the diagram that best fits the data. This line
reflects the RIR value: if the line is increasing the RIR value for this rubric
category is positive, and if the line is decreasing the RIR value is negative.

Relative statistics
-------------------

Because it is common to compare datasets of different sizes, all graphs display
their data as percentages of a total, rather than absolute numbers. This
behavior can be toggled with the :fa:`percent` button at the top of each chart.

Examples
--------

.. example:: Splitting on grades

    You want to find out if students with high grades submitted their work
    earlier to verify their work against the assignment's AutoTest setup.
    Let's say a high grade is a 7.5 or higher.

    Starting from the default filter, you uncheck the **Latest** option because
    you want the first submission of each student to be included.

    Next, you click the :fa:`scissors` button to split the filter, and you
    enter `7.5` in the **Grade** field.

    Finally, click the :fa:`check` button to apply the split. You now have two
    datasets, one with all submissions with a grade less than 7.5, and another
    with all submissions with a grade greater than 7.5.

    You can now navigate to the submission date graph to compare the two
    groups.

.. example:: Splitting on multiple criteria

    You want to perform the same experiment as in the previous example, but now
    you want to compare those results between two teaching assistants, Alice
    and Bob.

    Starting from the default filter, you click the :fa:`scissors` button,
    enter a 7.5 in the **Grade** field, and select both Alice and Bob in the
    **Graders** field.

    Clicking the :fa:`check` button now results in 4 datasets:

    - One with grades below 7.5 and graded by Alice
    - One with grades above 7.5 and graded by Alice
    - One with grades below 7.5 and graded by Bob
    - One with grades above 7.5 and graded by Bob

.. example:: Comparing between graders

    You want to see if there is a correlation between the amount of feedback
    given and the average grade between your teaching assistants.

    You start with the default filter and click the :fa:`scissors` button. In
    the **Graders** field you select "All". In the results below the split
    options you can see the average grade and the average number of inline
    feedback entries per TA.

    You click the :fa:`check` button to get more detailed information such as
    the grade distribution per teaching assistant.
