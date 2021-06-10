
/**
 * Toggle (show / hide) the sidebar menu on small screens when the hamburger
 * menu button has been clicked.
 */
function toggleMenu() {
    var menu = document.getElementById("menuPanel");

    if (menu.classList.contains('is-hidden-touch')) {
        menu.classList.replace('is-hidden-touch', 'is-full-touch');
    } else {
        menu.classList.replace('is-full-touch', 'is-hidden-touch');
    }
}

/**
 * Expand the element in the sidebar to show its children.
 * @param {*} element The element to be expanded.
 */
function toggleExpand(element) {
    var ul = element.parentElement.parentElement.getElementsByTagName("UL")[0];
    var i = element.firstChild.nextSibling;

    if (ul.classList.contains('is-expanded')) {
        i.classList.replace('fa-angle-down', 'fa-angle-right');
        ul.classList.replace('is-expanded', 'is-collapsed');
    } else {
        i.classList.replace('fa-angle-right', 'fa-angle-down');
        ul.classList.replace('is-collapsed', 'is-expanded');
    }
}

/**
 * Active the overlay containing the search bar and search results.
 */
function showSearchOverlay() {
    document.getElementById("search").classList.add("is-active")
    searchbar = document.getElementById("searchbar")
    searchbar.focus()
    searchbar.select()

    // Prevent background from scrolling while search window is open.
    document.documentElement.style.overflow = 'hidden';
    document.body.scroll = "no";

    activateSearch()
}

/**
 * Hide the overlay containing the search bar and results.
 */
function hideSearchOverlay() {
    /* Hide the search bar overlay.
     */
    document.getElementById("search").classList.remove("is-active")

    // Allow background to scroll again.
    document.documentElement.style.overflow = 'scroll';
    document.body.scroll = "yes";
}

/**
 * Add an keyboard event listener to activate a search function
 * {@link performSearch} on every keystroke.
 */
function activateSearch() {
    /* Activate the search bar with an keyboard event listener.
     */
    const searchInput = document.getElementById("searchbar");
    const resultsWrapper = document.getElementById("search-results")

    if (searchInput) {
        // Update search results when a key is pressed.
        searchInput.addEventListener('keyup', () => {
            let input = searchInput.value;
            if (input.length) {
                let searcher = performSearch(input);
                renderResults(input, searcher, resultsWrapper);
            } else {
                resultsWrapper.innerHTML = '';
            }
        })
    }
}

/**
 * Create a <div> element containing the necessary HTML code to display the
 * data of the results.
 * @param {*} url The url of the Result page.
 * @param {*} title The title of the Result page.
 * @param {*} content The content that should be displayed under the title.
 * @returns An HTML element, the container of the result entry.
 */
function createResultElement(url, title, content) {
    var element = document.createElement('div');
    element.innerHTML = `<a class="panel-block result is-flex-direction-column"
                         href="${url}"><h1 class="result-title"><strong>
                         ${title}</strong></h1><p class="result-content">
                         ${content}</p></a>`;

    return element;
}

function highlightSearchQuery(query, text) {
    var highlighter = '<span class="has-background-primary-light has-text-primary">';
    var index = text.search(new RegExp(query, "i"));
    if (index < 0) {
        return "";
    }

    var target = text.slice(index, index + query.length);
    var displayText = text.slice(Math.abs(index - 50), index) +
                      highlighter + target + "</span>" +
                      text.slice(index + query.length, index + 100);

    return displayText.slice(displayText.indexOf(' '), displayText.lastIndexOf(' ')) + ' ...';
}

/**
 * Display the results acquired by the search function {@link performSearch}
 * inside the HTML page alongside some text found in the appropriate pages.
 * @param {*} searcher The generator which yields the search results.
 * @param {*} resultsWrapper The html element in which the results are to be
 *     placed.
 */
function renderResults(query, searcher, resultsWrapper) {
    resultsWrapper.innerHTML = '<ul id="result-list"></ul>';
    var resultList = document.getElementById('result-list');
    var parser = new DOMParser();

    var i = 0;
    for (let r of searcher) {
        // Limit number of search results for now.
        if (i++ > 10) {
            break;
        }

        // Display text containing the searched word(s).
        // TODO: improve / speed up.
        fetch('../' + r.page)
            .then(res => res.text())
            .then(data => {
                var html = parser.parseFromString(data, 'text/html');
                var text = html.getElementById('content').innerText;
                var displayText = highlightSearchQuery(query, text);
                resultEl = createResultElement('../' + r.page, r.title, displayText);
                resultList.append(resultEl);
            })
            .catch(console.error);
    }
}
