
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

function toggleExpand(element) {
    /* Toggle the expansion of an element in the siddebar.
     */
    var ul = element.parentElement.parentElement.getElementsByTagName("UL")[0];
    var i = element.firstChild.nextSibling;
    console.log(i);
    if (ul.classList.contains('is-expanded')) {
        i.classList.replace('fa-angle-down', 'fa-angle-right');
        ul.classList.replace('is-expanded', 'is-collapsed');
    } else {
        i.classList.replace('fa-angle-right', 'fa-angle-down');
        ul.classList.replace('is-collapsed', 'is-expanded');
    }
}

function showSearchOverlay() {
    /* Active the search bar overlay.
     */
    document.getElementById("search").classList.add("is-active")
    searchbar = document.getElementById("searchbar")
    searchbar.focus()
    searchbar.select()

    // Prevent background from scrolling while search window is open.
    document.documentElement.style.overflow = 'hidden';
    document.body.scroll = "no";

    activateSearch()
}

function hideSearchOverlay() {
    /* Hide the search bar overlay.
     */
    document.getElementById("search").classList.remove("is-active")

    // Allow background to scroll again.
    document.documentElement.style.overflow = 'scroll';
    document.body.scroll = "yes";
}

function activateSearch() {
    /* Activate the search bar with an event listener.
     */
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

function renderResults(searcher, resultsWrapper) {
    /* Render the title of the search results aswell as a little bit
     * (200 characters) of text contained in the article.
     */
    let content = '';
    resultsWrapper.innerHTML = '<ul id="result-list"></ul>';

    for (let r of searcher) {
        id = r.title.replace(/ /g, "-");
        resultEl = `<div id="${id}"><a class="panel-block result is-flex-direction-column" href="../${r.page}">
                    <h1 class="result-title"><strong>${r.title}</strong></h1>
                    <p class="result-content"></p></a></div>`

        $('#result-list').append(resultEl);

        // Send ajax request to get text from the page.
        $.ajax({
            url: `../${r.page}`,
            title: `${r.title}`,
            type: 'get',
            dataType: 'html',
            success: function(data) {
                var html_data = $(data);

                // If no text is found, don't show any page content.
                try {
                    var p_text = $("#content p", html_data)[0].textContent;
                } catch (error) {
                    return;
                }

                id = this.title.replace(/ /g, "-");
                $("#" + id + " .result-content").text($.trim(p_text).substr(0, 200) + "...");
            }
        });
    }

}