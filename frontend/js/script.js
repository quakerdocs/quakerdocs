
const ROOT = document.location.hostname

function toggleFunction() {
    /* Used to toggle the menu on small screens when clicking on the menu
     * button.
     */
    var x = document.getElementById("mini-menu");
    if (x.className.indexOf("hide") == -1) {
        x.className = x.className.replace("", "hide");
    } else {
        x.className = x.className.replace("hide", "");
    }
}

function showSearchOverlay() {
    document.getElementById("search").classList.add("is-active")

    // Prevent background from scrolling while search window is open.
    document.documentElement.style.overflow = 'hidden';
    document.body.scroll = "no";

    activateSearch()
}

function hideSearchOverlay() {
    document.getElementById("search").classList.remove("is-active")

    // Allow background to scroll again.
    document.documentElement.style.overflow = 'scroll';
    document.body.scroll = "yes";
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
        // Update search results when a key is pressed.
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

function renderResults(searcher, resultsWrapper) {
    /* Render the title of the search results aswell as a little bit
     * (200 characters) of text contained in the article.
     */
    let content = '';
    for (let r of searcher) {
        let text = "";

        // Send ajax request to get text from the page.
        $.ajax({
            url: `../${r.page}`,
            type: 'get',
            dataType: 'html',
            async: false,
            success: function(data) {
                var html_data = $(data);

                // If no text is found, keep an empty string.
                try {
                    var p_text = $("#content p", html_data)[0].textContent
                } catch (error) {
                    return;
                }

                text = $.trim(p_text).substr(0, 200) + "...";
            }
        });

        content += `<div onclick="location.href='../${r.page}'" class="result"><h1 class="result-title"><strong>
                    ${r.title}</strong></h1><p class="result-content">${text}</p></div>`
    }

    resultsWrapper.innerHTML = `<ul>${content}</ul>`;
}