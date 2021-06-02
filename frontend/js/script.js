
var ROOT = document.location.hostname
// Used to toggle the menu on small screens when clicking on the menu button
function toggleFunction() {
    var x = document.getElementById("mini-menu");
    if (x.className.indexOf("hide") == -1) {
        x.className = x.className.replace("", "hide");
    } else {
        x.className = x.className.replace("hide", "");
    }
}

function showSearchOverlay() {
    document.getElementById("search").classList.add("is-active")
    activateSearch()
}

function hideSearchOverlay() {
    document.getElementById("search").classList.remove("is-active")
}

class Result {
    constructor(page, title, paragraph="") {
        // The page URL.
        this.page = page;

        // The title of the page, for quick display.
        this.title = title;

        // Optionally the paragraph title, to allow searching on paragraph level.
        // This is a stretch goal, so it doesn't have to be supported right away.
        this.paragraph = paragraph;
    }
};

function activateSearch() {
    const searchInput = document.getElementById("searchbar");
    const resultsWrapper = document.getElementById("search-results")

    if (searchInput) {
        searchInput.addEventListener('keyup', () => {
            let input = searchInput.value;
            if (input.length) {
                let searcher = performSearch(input);
                renderResults(searcher, resultsWrapper);
            } else {
                resultsWrapper.innerHTML = '';
            }
        })
    }
}

function* performSearch(query) {
    // Nothing is done with query as of now.

    let n_pages = Math.floor(Math.random() * 5) + 1;

    random_pages = [
        new Result("index.html", "Index"),
        new Result("about/about.html", "About"),
        new Result("guides/autotest-best-practices.html", "autotest best practices"),
        new Result("guides/cannot-find-feature-in-codegrade.html", "cannot find feature in codegrade"),
        new Result("guides/checking-for-plagiarism.html", "checking for plagiarism"),
        new Result("guides/creating-an-assignment.html", "creating an assignment"),
        new Result("guides/creating-managing-and-using-snippets.html", "creating managing and using snippets"),
        new Result("guides/dividing-submissions.html", "dividing submissions"),
        new Result("guides/enabling-continuous-feedback-for-an-assignment.html", "enabling continuous feedback for an assignment"),
        new Result("guides/getting-started-with-codegrade.html", "getting started with codegrade"),
        new Result("guides/installing-codegrade-filesystem.html", "installing codegrade filesystem"),
        new Result("guides/pass-back-grades-to-canvas-blackboard-moodle-brightspace.html", "pass back grades to canvas blackboard moodle brightspace"),
        new Result("guides/setting-up-autotest.html", "setting up autotest"),
        new Result("guides/setting-up-git-uploads.html", "setting up git uploads"),
        new Result("guides/setting-up-hand-in-requirements.html", "setting up hand in requirements"),
        new Result("guides/set-up-a-rubric-for-an-assignment.html", "set up a rubric for an assignment"),
        new Result("guides/set-up-group-assignment.html", "set up group assignment"),
        new Result("guides/setup-password-for-codegrade-account.html", "setup password for codegrade account"),
        new Result("guides/use-codegrade-as-a-student.html", "use codegrade as a student"),
        new Result("guides/use-codegrade-filesystem.html", "use codegrade filesystem"),
        new Result("guides/using-shortcuts.html", "using shortcuts")
    ];

    for (i = 0; i < n_pages; i++) {
        yield random_pages[Math.floor(Math.random() * random_pages.length)];
    }
}

var text;
function renderResults(searcher, resultsWrapper) {
    let content = '';
    for (let r of searcher) {
        var text = null;
        $.ajax({
            url: `../${r.page}`,
            type: 'get',
            dataType: 'html',
            async: false,
            success: function(data) {
                var html_data = $(data);
                var p_text = $("#content p", html_data)[0].textContent

                text = $.trim(p_text);
            }
        });

        console.log(text);
        content += `<a href="../${r.page}" class="panel-block"><h1>${r.title}</h1>
                    <p>${text}</p></a>`
    }

    resultsWrapper.innerHTML = `<ul>${content}</ul>`;
}