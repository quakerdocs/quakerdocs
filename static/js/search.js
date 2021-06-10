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
