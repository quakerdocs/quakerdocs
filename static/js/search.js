/**
 * Class representing a result entry.
 */
class Result {
    /**
     * Create a new Result entry.
     * @constructor
     * @param {*} page The URL to the result page.
     * @param {*} title The title of the result page.
     * @param {*} paragraph The paragraph title (STRETCH GOAL)
     */
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

/* Keep track if the webassambly module has completed loading. */
var wasmLoaded = false;
Module['onRuntimeInitialized'] = function() {
    wasmLoaded = true;
}

/**
 * Perform a search action and yield the results to the HTML page.
 * @param {*} query The query the search should be performed on.
 * @returns {null} Nothing if no results were found.
 * @yields {Result} The next search result entry.
 */
function* performSearch(query) {
    if (!wasmLoaded)
        return;

    /* Get the functions from the wasm module. */
    var search = Module.cwrap('performSearch', null, ['string']);
    var getres = Module.cwrap('getSearch', 'string');

    /* Perform the search. */
    search(query);

    /* Return the results as they are asked. */
    while (result = getres()) {
        /* Split on new line, regex to work on all os'es. */
        let sep = result.split("\n");
        yield new Result(sep[0], sep[1], sep[2]);
    }
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
    var textBefore = text.slice(Math.abs(index - 50), index);
    var textAfter = text.slice(index + query.length, index + 100);
    var displayText = textBefore + highlighter + target + "</span>" + textAfter;
    var endIndex = displayText.lastIndexOf(' ');
    var startIndex = 0;
    if (textBefore) {
        startIndex = displayText.indexOf(' ');
    }

    return displayText.slice(startIndex, endIndex) + ' ...';
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
        if (i++ > 8) {
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
