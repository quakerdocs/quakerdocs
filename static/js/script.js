
function toggleMenu() {
    /* Used to toggle the menu on small screens when clicking on the menu
     * button.
     */
    var menu = document.getElementById("menuPanel");

    if (menu.classList.contains('is-hidden-touch')) {
        menu.classList.replace('is-hidden-touch', 'is-full');
    } else {
        menu.classList.replace('is-full', 'is-hidden-touch');
    }
}

function toggleExpand(element) {
    /* Toggle the expansion of an element in the sidebar.
     */
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

function createResultElement(url, title, content) {
    var element = document.createElement('div');
    element.innerHTML = `<a class="panel-block result is-flex-direction-column" href="${url}">
        <h1 class="result-title"><strong>${title}</strong></h1>
        <p class="result-content">${content}</p></a>`;

    return element;
}

function renderResults(searcher, resultsWrapper) {
    resultsWrapper.innerHTML = '<ul id="result-list"></ul>';
    var resultList = document.getElementById('result-list');
    var parser = new DOMParser();

    for (let r of searcher) {
        var url = '../' + r.page;
        fetch(url)
            .then(res => res.text())
            .then(data => {
                var html = parser.parseFromString(data, 'text/html');
                var pTags = html.getElementById('content').getElementsByTagName('p');
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
