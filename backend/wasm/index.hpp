#include <unordered_map>
#include <vector>

/* Child and page sizes. */
typedef int child_s;
typedef int page_s;

/* Int as pointers. */
typedef int char_p;
typedef int child_p;
typedef int page_p;

/* A node of the Radix tree. */
struct Node {
    char_p chars;
    child_p children;
    page_p pages;
    /* The number of children. */
    child_s child_count;
    /* The number of pages. Is zero when this node is not an end. */
    page_s page_count;
};

/* Struct storing the data associated with a page. */
struct Page {
    short page_index;
    short count;
};

const char *urltitles[] = {"index.html\nThe CodeGrade Documentation\n","api.html\nAPI\n","about/authors.html\nCodeGrade Team\n","about/codegradefeatures.html\n\n","about/contact.html\nContact Us\n","about/history.html\nHistory of CodeGrade\n","about/whatis.html\nWhat is CodeGrade?\n","about/about.html\nAbout CodeGrade\n","about/changelog.html\nChangelog\n","about/contributing.html\nContributing to CodeGrade\n","about/technologies.html\nUsed Technologies\n","psef_api/psef.html\nSource code documentation of \n","user/management.html\nCourse and Assignment Management\n","user/permissions.html\nPermissions\n","user/analytics-dashboard.html\nAnalytics Dashboard\n","user/groups.html\nGroups\n","user/notifications.html\nNotifications\n","user/codeviewer.html\nCode Viewer\n","user/overview.html\nOverview of CodeGrade\n","user/preferences.html\nSettings and Site Preferences\n","user/plagiarism.html\nPlagiarism Detection\n","user/exam-mode.html\nExam mode\n","user/lms.html\nLMS Integration\n","user/autotest/running-autotest.html\nRunning AutoTest\n","user/autotest/categories.html\nCategories\n","user/autotest/setup.html\nSetup\n","user/autotest/student-experience.html\nStudent Experience\n","user/autotest/levels.html\nLevels\n","user/autotest/overview.html\nAutoTest\n","user/autotest/tests.html\nTests\n","user/autotest/continuous-feedback.html\nContinuous Feedback\n","guides/setting-up-unittest.html\nSetting up Unit Tests\n","guides/creating-a-standalone-assignment.html\nCreate a standalone CodeGrade assignment\n","guides/getting-started-with-codegrade.html\nGetting started with CodeGrade\n","guides/creating-an-assignment.html\nCreate a CodeGrade assignment\n","guides/creating-a-brightspace-assignment.html\nCreate a CodeGrade assignment in BrightSpace\n","guides/use-codegrade-filesystem.html\nUse the CodeGrade Filesystem to locally mount CodeGrade\n","guides/setting-up-checkpoints.html\nSetting up Checkpoints\n","guides/cannot-find-feature-in-codegrade.html\nI cannot find a feature in CodeGrade\n","guides/creating-a-blackboard-assignment.html\nCreate a CodeGrade assignment in Blackboard\n","guides/creating-an-open-edx-assignment.html\nCreate a CodeGrade assignment in Open edX\n","guides/checking-for-plagiarism.html\nCheck for plagiarism in a CodeGrade assignment\n","guides/getting-started-with-codegrade-in-brightspace.html\nGetting started with CodeGrade in BrightSpace\n","guides/getting-started-with-codegrade-in-blackboard.html\nGetting started with CodeGrade in Blackboard\n","guides/creating-managing-and-using-snippets.html\nCreate, manage and use snippets\n","guides/using-shortcuts.html\nUsing shortcuts\n","guides/getting-started-with-codegrade-in-canvas.html\nGetting started with CodeGrade in Canvas\n","guides/getting-started-introduction.html\nIntroduction\n","guides/set-up-group-assignment.html\nSet up a CodeGrade group assignment\n","guides/installing-codegrade-filesystem.html\nInstall the CodeGrade Filesystem\n","guides/dividing-submissions.html\nDivide submissions over graders\n","guides/setting-up-capturepointstest.html\nSetting up Capture Points Tests\n","guides/autotest-best-practices.html\nBest Practices for AutoTest\n","guides/getting-started-with-codegrade-in-sakai.html\nGetting started with CodeGrade in Sakai\n","guides/pass-back-grades-to-canvas-blackboard-moodle-brightspace.html\nPass back grades to Canvas, Blackboard, Moodle or Brightspace\n","guides/setting-up-iotest.html\nSetting up IO Tests\n","guides/getting-started-with-codegrade-in-moodle.html\nGetting started with CodeGrade in Moodle\n","guides/setting-up-codequalitytest.html\nSetting up Code Quality tests\n","guides/setup-password.html\nWarning\n","guides/creating-a-canvas-assignment.html\nCreate a CodeGrade assignment in Canvas\n","guides/setup-password-for-codegrade-account.html\nSet up a password for my CodeGrade account\n","guides/setting-up-runprogramtest.html\nSetting up Run Program Tests\n","guides/setting-up-hand-in-requirements.html\nSet up hand-in requirements for a CodeGrade assignment\n","guides/creating-a-moodle-assignment.html\nCreate a CodeGrade assignment in Moodle\n","guides/enabling-continuous-feedback-for-an-assignment.html\nEnabling Continuous Feedback for an assignment\n","guides/getting-started-with-codegrade-standalone.html\nGetting started with CodeGrade Standalone\n","guides/setting-up-git-uploads.html\nSet up Git uploads for a CodeGrade assignment\n","guides/set-up-a-rubric-for-an-assignment-old.html\nSet up a rubric for an assignment\n","guides/getting-started-with-codegrade-in-open-edx.html\nGetting started with CodeGrade in Open edX\n","guides/set-up-a-rubric-for-an-assignment.html\nSet up a rubric for an assignment\n","guides/use-codegrade-as-a-student.html\nHow to use CodeGrade as a student\n","guides/setting-up-autotest.html\nSetting up AutoTest\n","guides/includes/getting-started-general.html\nGraders\n"};

const char node_data[] = {0,0,0,0,52,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,208,0,0,0,1,0,0,0,0,0,0,0,3,0,0,0,2,0,0,0,208,0,0,0,0,0,0,0,4,0,0,0,5,0,0,0,0,0,0,0,216,0,0,0,1,0,0,0,4,0,0,0,10,0,0,0,0,0,0,0,216,0,0,0,1,0,0,0,8,0,0,0,14,0,0,0,2,0,0,0,216,0,0,0,0,0,0,0,12,0,0,0,16,0,0,0,0,0,0,0,224,0,0,0,1,0,0,0,12,0,0,0,19,0,0,0,0,0,0,0,224,0,0,0,1,0,0,0,16,0,0,0,23,0,0,0,2,0,0,0,224,0,0,0,0,0,0,0,20,0,0,0,25,0,0,0,2,0,0,0,232,0,0,0,0,0,0,0,20,0,0,0,27,0,0,0,0,0,0,0,240,0,0,0,1,0,0,0,20,0,0,0,32,0,0,0,0,0,0,0,240,0,0,0,1,0,0,0,24,0,0,0,36,0,0,0,0,0,0,0,240,0,0,0,1,0,0,0,28,0,0,0,43,0,0,0,2,0,0,0,240,0,0,0,0,0,0,0,32,0,0,0,45,0,0,0,2,0,0,0,248,0,0,0,0,0,0,0,32,0,0,0,47,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,32,0,0,0,54,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,36,0,0,0,58,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,40,0,0,0,62,0,0,0,2,0,0,0,0,1,0,0,0,0,0,0,44,0,0,0,64,0,0,0,0,0,0,0,8,1,0,0,1,0,0,0,44,0,0,0,69,0,0,0,0,0,0,0,8,1,0,0,1,0,0,0,48,0,0,0,73,0,0,0,2,0,0,0,8,1,0,0,0,0,0,0,52,0,0,0,75,0,0,0,2,0,0,0,16,1,0,0,0,0,0,0,52,0,0,0,78,0,0,0,0,0,0,0,24,1,0,0,1,0,0,0,52,0,0,0,81,0,0,0,0,0,0,0,24,1,0,0,1,0,0,0,56,0,0,0,83,0,0,0,0,0,0,0,24,1,0,0,1,0,0,0,60,0,0,0,90,0,0,0,2,0,0,0,24,1,0,0,0,0,0,0,64,0,0,0,92,0,0,0,0,0,0,0,32,1,0,0,1,0,0,0,64,0,0,0,95,0,0,0,0,0,0,0,32,1,0,0,1,0,0,0,68,0,0,0,102,0,0,0,2,0,0,0,32,1,0,0,0,0,0,0,72,0,0,0,104,0,0,0,0,0,0,0,40,1,0,0,1,0,0,0,72,0,0,0,113,0,0,0,0,0,0,0,40,1,0,0,1,0,0,0,76,0,0,0,117,0,0,0,2,0,0,0,40,1,0,0,0,0,0,0,80,0,0,0,119,0,0,0,0,0,0,0,48,1,0,0,1,0,0,0,80,0,0,0,123,0,0,0,0,0,0,0,48,1,0,0,1,0,0,0,84,0,0,0,131,0,0,0,2,0,0,0,48,1,0,0,0,0,0,0,88,0,0,0,133,0,0,0,0,0,0,0,56,1,0,0,1,0,0,0,88,0,0,0,140,0,0,0,0,0,0,0,56,1,0,0,1,0,0,0,92,0,0,0,146,0,0,0,0,0,0,0,56,1,0,0,1,0,0,0,96,0,0,0,148,0,0,0,2,0,0,0,56,1,0,0,0,0,0,0,100,0,0,0,150,0,0,0,2,0,0,0,64,1,0,0,0,0,0,0,100,0,0,0,152,0,0,0,2,0,0,0,72,1,0,0,0,0,0,0,100,0,0,0,154,0,0,0,0,0,0,0,80,1,0,0,1,0,0,0,100,0,0,0,158,0,0,0,0,0,0,0,80,1,0,0,1,0,0,0,104,0,0,0,161,0,0,0,0,0,0,0,80,1,0,0,1,0,0,0,108,0,0,0,164,0,0,0,0,0,0,0,80,1,0,0,1,0,0,0,112,0,0,0,171,0,0,0,2,0,0,0,80,1,0,0,0,0,0,0,116,0,0,0,173,0,0,0,2,0,0,0,88,1,0,0,0,0,0,0,116,0,0,0,175,0,0,0,0,0,0,0,96,1,0,0,1,0,0,0,116,0,0,0,178,0,0,0,0,0,0,0,96,1,0,0,1,0,0,0,120,0,0,0,182,0,0,0,0,0,0,0,96,1,0,0,1,0,0,0,124,0,0,0,188,0,0,0,2,0,0,0,96,1,0,0,0,0,0,0,128,0,0,0,190,0,0,0,0,0,0,0,104,1,0,0,1,0,0,0,128,0,0,0,196,0,0,0,0,0,0,0,104,1,0,0,1,0,0,0,132,0,0,0,202,0,0,0,2,0,0,0,104,1,0,0,0,0,0,0,136,0,0,0,204,0,0,0,0,0,0,0,112,1,0,0,1,0,0,0,136,0,0,0,206,0,0,0,0,0,0,0,112,1,0,0,1,0,0,0,140,0,0,0,209,0,0,0,2,0,0,0,112,1,0,0,0,0,0,0,144,0,0,0,211,0,0,0,0,0,0,0,120,1,0,0,1,0,0,0,144,0,0,0,216,0,0,0,0,0,0,0,120,1,0,0,1,0,0,0,148,0,0,0,222,0,0,0,2,0,0,0,120,1,0,0,0,0,0,0,152,0,0,0,224,0,0,0,0,0,0,0,128,1,0,0,1,0,0,0,152,0,0,0,228,0,0,0,0,0,0,0,128,1,0,0,1,0,0,0,156,0,0,0,231,0,0,0,2,0,0,0,128,1,0,0,0,0,0,0,160,0,0,0,233,0,0,0,2,0,0,0,136,1,0,0,0,0,0,0,160,0,0,0,235,0,0,0,0,0,0,0,144,1,0,0,1,0,0,0,160,0,0,0,242,0,0,0,0,0,0,0,144,1,0,0,1,0,0,0,164,0,0,0,247,0,0,0,0,0,0,0,144,1,0,0,1,0,0,0,168,0,0,0,252,0,0,0,2,0,0,0,144,1,0,0,0,0,0,0,172,0,0,0,254,0,0,0,0,0,0,0,152,1,0,0,1,0,0,0,172,0,0,0,2,1,0,0,0,0,0,0,152,1,0,0,1,0,0,0,176,0,0,0,9,1,0,0,2,0,0,0,152,1,0,0,0,0,0,0,180,0,0,0,11,1,0,0,0,0,0,0,160,1,0,0,1,0,0,0,180,0,0,0,15,1,0,0,0,0,0,0,160,1,0,0,1,0,0,0,184,0,0,0,18,1,0,0,2,0,0,0,160,1,0,0,0,0,0,0,188,0,0,0,20,1,0,0,2,0,0,0,168,1,0,0,0,0,0,0,188,0,0,0,22,1,0,0,0,0,0,0,176,1,0,0,1,0,0,0,188,0,0,0,25,1,0,0,0,0,0,0,176,1,0,0,1,0,0,0,192,0,0,0,27,1,0,0,0,0,0,0,176,1,0,0,1,0,0,0,196,0,0,0,32,1,0,0,2,0,0,0,176,1,0,0,0,0,0,0,200,0,0,0,34,1,0,0,0,0,0,0,184,1,0,0,1,0,0,0,200,0,0,0,39,1,0,0,0,0,0,0,184,1,0,0,1,0,0,0,204,0,0,0,45,1,0,0,2,0,0,0,184,1,0,0,0,0,0,0,208,0,0,0,47,1,0,0,0,0,0,0,192,1,0,0,1,0,0,0,208,0,0,0,70,1,0,0,0,0,0,0,192,1,0,0,1,0,0,0,212,0,0,0,73,1,0,0,2,0,0,0,192,1,0,0,0,0,0,0,216,0,0,0,75,1,0,0,0,0,0,0,200,1,0,0,1,0,0,0,216,0,0,0,80,1,0,0,0,0,0,0,200,1,0,0,1,0,0,0,220,0,0,0,84,1,0,0,2,0,0,0,200,1,0,0,0,0,0,0,224,0,0,0,86,1,0,0,0,0,0,0,208,1,0,0,1,0,0,0,224,0,0,0,89,1,0,0,0,0,0,0,208,1,0,0,1,0,0,0,228,0,0,0,92,1,0,0,2,0,0,0,208,1,0,0,0,0,0,0,232,0,0,0,94,1,0,0,0,0,0,0,216,1,0,0,1,0,0,0,232,0,0,0,96,1,0,0,0,0,0,0,216,1,0,0,1,0,0,0,236,0,0,0,100,1,0,0,0,0,0,0,216,1,0,0,1,0,0,0,240,0,0,0,102,1,0,0,2,0,0,0,216,1,0,0,0,0,0,0,244,0,0,0,104,1,0,0,1,0,0,0,224,1,0,0,0,0,0,0,244,0,0,0,107,1,0,0,0,0,0,0,228,1,0,0,1,0,0,0,244,0,0,0,109,1,0,0,0,0,0,0,228,1,0,0,1,0,0,0,248,0,0,0,112,1,0,0,2,0,0,0,228,1,0,0,0,0,0,0,252,0,0,0,114,1,0,0,2,0,0,0,236,1,0,0,0,0,0,0,252,0,0,0,116,1,0,0,1,0,0,0,244,1,0,0,0,0,0,0,252,0,0,0,122,1,0,0,0,0,0,0,248,1,0,0,1,0,0,0,252,0,0,0,124,1,0,0,0,0,0,0,248,1,0,0,1,0,0,0,0,1,0,0,130,1,0,0,0,0,0,0,248,1,0,0,1,0,0,0,4,1,0,0,138,1,0,0,0,0,0,0,248,1,0,0,1,0,0,0,8,1,0,0,140,1,0,0,0,0,0,0,248,1,0,0,1,0,0,0,12,1,0,0,142,1,0,0,2,0,0,0,248,1,0,0,0,0,0,0,16,1,0,0,144,1,0,0,0,0,0,0,0,2,0,0,1,0,0,0,16,1,0,0,149,1,0,0,0,0,0,0,0,2,0,0,1,0,0,0,20,1,0,0,152,1,0,0,1,0,0,0,0,2,0,0,0,0,0,0,24,1,0,0,154,1,0,0,0,0,0,0,4,2,0,0,1,0,0,0,24,1,0,0,156,1,0,0,0,0,0,0,4,2,0,0,1,0,0,0,28,1,0,0,158,1,0,0,0,0,0,0,4,2,0,0,1,0,0,0,32,1,0,0,162,1,0,0,0,0,0,0,4,2,0,0,1,0,0,0,36,1,0,0,166,1,0,0,0,0,0,0,4,2,0,0,1,0,0,0,40,1,0,0,170,1,0,0,0,0,0,0,4,2,0,0,1,0,0,0,44,1,0,0,174,1,0,0,0,0,0,0,4,2,0,0,1,0,0,0,48,1,0,0,177,1,0,0,0,0,0,0,4,2,0,0,1,0,0,0,52,1,0,0,180,1,0,0,2,0,0,0,4,2,0,0,0,0,0,0,56,1,0,0,183,1,0,0,0,0,0,0,12,2,0,0,1,0,0,0,56,1,0,0,190,1,0,0,0,0,0,0,12,2,0,0,1,0,0,0,60,1,0,0,196,1,0,0,0,0,0,0,12,2,0,0,1,0,0,0,64,1,0,0,202,1,0,0,0,0,0,0,12,2,0,0,1,0,0,0,68,1,0,0,208,1,0,0,0,0,0,0,12,2,0,0,1,0,0,0,72,1,0,0,215,1,0,0,0,0,0,0,12,2,0,0,1,0,0,0,76,1,0,0,223,1,0,0,0,0,0,0,12,2,0,0,1,0,0,0,80,1,0,0,229,1,0,0,0,0,0,0,12,2,0,0,1,0,0,0,84,1,0,0,238,1,0,0,0,0,0,0,12,2,0,0,1,0,0,0,88,1,0,0,246,1,0,0,0,0,0,0,12,2,0,0,1,0,0,0,92,1,0,0,253,1,0,0,2,0,0,0,12,2,0,0,0,0,0,0,96,1,0,0,2,2,0,0,0,0,0,0,20,2,0,0,1,0,0,0,96,1,0,0,5,2,0,0,0,0,0,0,20,2,0,0,1,0,0,0,100,1,0,0,7,2,0,0,2,0,0,0,20,2,0,0,0,0,0,0,104,1,0,0,10,2,0,0,0,0,0,0,28,2,0,0,1,0,0,0,104,1,0,0,15,2,0,0,0,0,0,0,28,2,0,0,1,0,0,0,108,1,0,0};

const char children_data[] = {38,0,0,0,116,0,0,0,88,0,0,0,1,0,0,0,118,0,0,0,94,0,0,0,105,0,0,0,114,0,0,0,91,0,0,0,117,0,0,0,112,0,0,0,110,0,0,0,106,0,0,0,113,0,0,0,35,0,0,0,129,0,0,0,57,0,0,0,13,0,0,0,8,0,0,0,51,0,0,0,32,0,0,0,21,0,0,0,130,0,0,0,29,0,0,0,63,0,0,0,85,0,0,0,122,0,0,0,74,0,0,0,2,0,0,0,39,0,0,0,60,0,0,0,123,0,0,0,79,0,0,0,127,0,0,0,18,0,0,0,126,0,0,0,99,0,0,0,119,0,0,0,46,0,0,0,26,0,0,0,128,0,0,0,5,0,0,0,125,0,0,0,54,0,0,0,68,0,0,0,133,0,0,0,71,0,0,0,124,0,0,0,107,0,0,0,115,0,0,0,82,0,0,0,95,0,0,0,3,0,0,0,4,0,0,0,6,0,0,0,7,0,0,0,9,0,0,0,12,0,0,0,10,0,0,0,11,0,0,0,14,0,0,0,17,0,0,0,15,0,0,0,16,0,0,0,20,0,0,0,19,0,0,0,25,0,0,0,22,0,0,0,24,0,0,0,23,0,0,0,27,0,0,0,28,0,0,0,31,0,0,0,30,0,0,0,34,0,0,0,33,0,0,0,37,0,0,0,36,0,0,0,40,0,0,0,45,0,0,0,44,0,0,0,41,0,0,0,43,0,0,0,42,0,0,0,47,0,0,0,50,0,0,0,48,0,0,0,49,0,0,0,53,0,0,0,52,0,0,0,55,0,0,0,56,0,0,0,58,0,0,0,59,0,0,0,61,0,0,0,62,0,0,0,64,0,0,0,67,0,0,0,65,0,0,0,66,0,0,0,70,0,0,0,69,0,0,0,73,0,0,0,72,0,0,0,75,0,0,0,78,0,0,0,76,0,0,0,77,0,0,0,80,0,0,0,81,0,0,0,84,0,0,0,83,0,0,0,87,0,0,0,86,0,0,0,89,0,0,0,90,0,0,0,92,0,0,0,93,0,0,0,96,0,0,0,98,0,0,0,97,0,0,0,100,0,0,0,104,0,0,0,103,0,0,0,101,0,0,0,102,0,0,0,109,0,0,0,108,0,0,0,111,0,0,0,121,0,0,0,120,0,0,0,132,0,0,0,131,0,0,0,135,0,0,0,134,0,0,0};

const char page_data[] = {72,0,1,0,72,0,3,0,72,0,7,0,72,0,2,0,72,0,3,0,72,0,3,0,72,0,4,0,72,0,5,0,72,0,6,0,72,0,7,0,72,0,15,0,72,0,3,0,72,0,6,0,72,0,3,0,72,0,4,0,72,0,4,0,72,0,6,0,72,0,7,0,72,0,1,0,72,0,2,0,72,0,3,0,72,0,19,0,72,0,3,0,72,0,7,0,72,0,1,0,72,0,2,0,72,0,3,0,72,0,3,0,72,0,6,0,72,0,1,0,72,0,1,0,72,0,12,0,72,0,2,0,72,0,3,0,72,0,1,0,72,0,9,0,72,0,1,0,72,0,4,0,72,0,1,0,72,0,1,0,72,0,2,0,72,0,2,0,72,0,5,0,71,0,2,0,72,0,1,0,72,0,1,0,72,0,2,0,70,0,1,0,70,0,1,0,71,0,1,0,72,0,1,0,72,0,2,0,68,0,1,0,70,0,2,0,68,0,1,0,70,0,1,0,71,0,1,0,72,0,1,0,20,0,2,0,52,0,1,0,72,0,1,0,52,0,1,0,70,0,1,0,56,0,2,0,57,0,4,0,65,0,2,0,71,0,1,0,52,0,2,0,29,0,1,0,29,0,2,0,71,0,1,0,25,0,1,0,25,0,1,0,25,0,1,0,31,0,2,0,52,0,1,0,52,0,1,0,52,0,1,0,68,0,2,0,71,0,1,0,72,0,1,0,72,0,1,0,72,0,3,0,72,0,4,0,72,0,6,0,72,0,7,0,72,0,10,0,72,0,10,0,72,0,5,0,72,0,10,0,72,0,1,0,72,0,10,0};

const char chars[] = "\02\0l\0evel\0ine\0t\0ab\0ype\0d\0i\0ffer\0vis\0isplay\0c\0o\0degrad\0urs\0ode\0p\0oint\0age\0g\0iv\0en\0e\0eneral\0s\0et\0nippet\0h\0ighlight\0elp\0f\0ill\0eedback\0a\0utomat\0mount\00\0m\0a\0n\0ual\0ag\0ke\0ultipl\0r\0e\0us\0vis\0ubric\0e\0xampl\0ffici\0u\0s\0se\0b\0lock\0utton\0n\0ame\0ew\0i\0n\0dividu\0tuit\0nlin\0v\0iew\0ersion\0w\0ork\0ay\0k\0e\0ep\0y\0nown\0o\0ften\0ption\0y\0ourinstitutioncodegrad\0et\0j\0upyt\0oin\01\000\075\05\00\0075\03\0z\0er\0o\0ip\0q\0u\0estio\0n\0aliti\0uestion\04\08\0x\0unit\0ml\07\05\06\0810\0422\0xml\0050\050\025\0qu\0estion\0aliti\0jupyt\0numer\0within\0teacher\0press\0overview\0submiss\0assign\0grad\0er\0e\0vi\0sibl\0ewer\0";

const Node *nodes = (Node *) node_data;
const child_p *children = (child_p *) node_data;
const Page *pages = (Page *) page_data;