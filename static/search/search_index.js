class Result {
    constructor(page, title, paragraph="") {
        /* The page URL. */
        this.page = page;

        /* The title of the page, for quick display. */
        this.title = title;

        /* Optionally the paragraph title, to allow searching on paragraph
        level. This is a stretch goal, so it doesn't have to be supported
        right away. */
        this.paragraph = paragraph;
    }
};


/* Function to use the wasm module to perform the search and return any
   results. */
function* performSearch(query) {

    /* Get the functions from the wasm module. */
    var search = Module.cwrap('performSearch', null, ['string']);
    var getres = Module.cwrap('getSearch', 'string');

    /* Perform the search. */
    search(query);

    /* Return the results as they are asked. */
    while (result = getres()) {
        /* Split on new line, regex to work on all os'es. */
        let sep = result.split(/\r\n|\n\r|\n|\r/);
        yield Result(sep[0], se[[1]]);
    }
}
