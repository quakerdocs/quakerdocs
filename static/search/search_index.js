
function* performSearch(query) {
    // TODO: check if the wasm has fully loaded.

    var search = Module.cwrap('performSearch', null, ['string']);
    var getres = Module.cwrap('getSearch', 'string');
    search(query);

    while (result = getres()) {
        // TODO: translate to Result object. (split it on \n)
        yield result;
    }
}
