
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

let searchOpen = false;

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

    searchOpen = true;
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

    searchOpen = false;
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
                renderResults(searcher, resultsWrapper);
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

/**
 * Display the results acquired by the search function {@link performSearch}
 * inside the HTML page alongside some text found in the appropriate pages.
 * @param {*} searcher The generator which yields the search results.
 * @param {*} resultsWrapper The html element in which the results are to be
 *     placed.
 */
function renderResults(searcher, resultsWrapper) {
    resultsWrapper.innerHTML = '<ul id="result-list"></ul>';
    var resultList = document.getElementById('result-list');
    var parser = new DOMParser();

    for (let r of searcher) {
        var url = '../' + r.page;

        // Retrieve the text out of the first <p> tag of the page.
        // TODO: Display text containing the searched word(s).
        fetch(url)
            .then(res => res.text())
            .then(data => {
                var html = parser.parseFromString(data, 'text/html');
                var pTags = html.getElementById('content')
                                .getElementsByTagName('p');
                var text = '';
                if (pTags) {
                    text = pTags[0].innerText.substring(0, 200);
                }
                text += ' ...';
                resultEl = createResultElement('../' + r.page, r.title, text);
                resultList.append(resultEl);
            })
            .catch(console.error);
    }
}
