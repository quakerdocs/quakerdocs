
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

/**
 * TODO: WTF DOES THIS DO
 * @param {*} results
 * @param {*} next
 * @returns
 */
function intersect(results, next) {
    if (results.length === 0) {
        return next;
    }

    let comb = [];

    for (let res of results) {
        for (let nex of next) {
            if (res[0] === nex[0]) {
                comb.push([res[0], res[1] + nex[1]]);
                break;
            }
        }
    }
    return comb;
}

/**
 * Perform a search action and yield the results to the HTML page.
 * @param {*} query The query the search should be performed on.
 * @returns {null} Nothing if no results were found.
 * @yields {Result} The next search result entry.
 */
function* performSearch(query) {
    var words = query.split(' ').map(stem);
    // console.log(words);
    var results = [];

    for (let word of words) {
        if (!(word in search_index))
            // Not in dict error
            return;

        results = intersect(results, search_index[word]);

        if (results.length === 0) {
            // No results found error.
            return;
        }
    }

    results.sort(function(a, b){ return a[1] - b[1] });

    // Yield all the pages in order of most occurences.
    for (let result of results) {
        let page_index = result[0];
        let page = search_urltitles[page_index];
        yield new Result(page[0], page[1]);
    }
}
