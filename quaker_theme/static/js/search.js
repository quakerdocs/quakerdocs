/* Keep track if the webassambly module has completed loading. */
let wasmLoaded = false
let searcher = null;

Module.onRuntimeInitialized = () => {
    wasmLoaded = true
}

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
    constructor (page, title, paragraph = '') {
        /* The page URL. */
        this.page = '../' + page

        /* The title of the page, for quick display. */
        this.title = title

        /* Optionally the paragraph title, to allow searching on paragraph level. */
        this.paragraph = paragraph

        /* The text with highlight to be added later. */
        this.content = ''
    }

    /**
     * Create a <div> element containing the necessary HTML code to display the
     * data of the results.
     * @param {*} url The url of the Result page.
     * @param {*} title The title of the Result page.
     * @param {*} content The content that should be displayed under the title.
     * @returns An HTML element, the container of the result entry.
     */
    createResultElement () {
        const element = document.createElement('div')
        element.innerHTML = `<a class="panel-block result is-flex-direction-column" href="${this.page}" onclick="storeSearchResults()">
                                <h1 class="result-title"><strong>${this.title}</strong></h1>
                                <p class="result-content">${this.content}</p>
                            </a>`

        return element
    }

};

/**
 * Perform a search action and yield the results to the HTML page.
 * @param {*} query The query the search should be performed on.
 * @returns {null} Nothing if no results were found.
 * @yields {Result} The next search result entry.
 */
function * performSearch (query) {
    if (!wasmLoaded) {
        return
    }

    /* Get the functions from the wasm module. */
    const search = Module.cwrap('performSearch', null, ['string'])
    const getres = Module.cwrap('getSearch', 'string')

    /* Perform the search. */
    search(query)

    /* Return the results as they are asked. */
    let result
    while (result = getres()) {
        /* Split on new line, regex to work on all os'es. */
        const sep = result.split('\n')
        yield new Result(sep[0], sep[1], sep[2])
    }
}

/**
 * Add an keyboard event listener to activate a search function
 * {@link performSearch} on every keystroke.
 */
function activateSearch () {
    /* Activate the search bar with an keyboard event listener.
     */
    const searchInput = document.getElementById('searchbar')
    const resultsWrapper = document.getElementById('search-results')
    const results = document.getElementById('search-results')

    if (searchInput) {
        // Update search results when a key is pressed.
        searchInput.addEventListener('keyup', () => {
            const input = searchInput.value

            if (input.length) {
                searcher = performSearch(input)
                renderResults(input, searcher, resultsWrapper)
            } else {
                resultsWrapper.innerHTML = ''
            }
        })
        results.addEventListener('scroll', () => {
            if (searcher == null)
                return;

            if (results.scrollTopMax - results.scrollTop < 90) {
                r = searcher.next()
                if (!r.done) {
                    let res = r.value.createResultElement()
                    document.getElementById('result-list').append(res)
                }
            }
        })
    }
}

/**
 * Display the results acquired by the search function {@link performSearch}
 * inside the HTML page alongside some text found in the appropriate pages.
 * @param {*} searcher The generator which yields the search results.
 * @param {*} resultsWrapper The html element in which the results are to be placed.
 */
function renderResults (query, searcher, resultsWrapper) {
    /* Reset the results and setup the parser */
    resultsWrapper.innerHTML = '<ul id="result-list"></ul>'
    const resultList = document.getElementById('result-list')
    const parser = new DOMParser()
    const maxResults = 15


    for (let i = 0; i <= maxResults; i++) {
        /* Limit number of search results. */
        r = searcher.next()
        if (r.done) {
            break
        }

        let res = r.value.createResultElement()
        document.getElementById('result-list').append(res)

        /* Fetch page contents. */
        // fetch('../' + r.page)
        //     .then(res => res.text())
        //     .then(data => {
        //         const html = parser.parseFromString(data, 'text/html')
        //         let href = '../' + r.page
        //         let text = html.getElementById('content').innerText
        //         /* Look for the section containing the result. */
        //         for (const section of html.querySelectorAll('section')) {
        //                 if (section.textContent.includes(query) && section.id) {
        //                         href += '#' + section.id
        //                         text = section.innerText
        //                         break
        //                     }
        //                 }

        //                 const displayText = highlightSearchQuery(query, text)
        //                 const resultEl = createResultElement(href, r.title, displayText)
        //                 resultList.append(resultEl)
        //             })
        //             .catch(console.error)
    }
}

/**
 * Highlights a query in the provided text using a span tag.
 * @param {*} query The query to be highlighted in the text.
 * @param {*} text The text.
 * @returns The text to be displayed containing the highlighted query.
 */
 function highlightSearchQuery (query, text) {
    const maxLenTextBefore = 50
    const maxLenTextAfter = 100
    const highlighter = '<span class="has-background-primary-light has-text-primary">'
    const index = text.search(new RegExp(query, 'i'))
    if (index < 0) {
        return ''
    }

    /* Slice out the target text and wrap it in a span tag. */
    const target = text.slice(index, index + query.length)
    const textBefore = text.slice(Math.max(index - maxLenTextBefore, 0), index)
    const textAfter = text.slice(index + query.length, index + maxLenTextAfter)
    const displayText = textBefore + highlighter + target + '</span>' + textAfter
    const endIndex = displayText.lastIndexOf(' ')
    let startIndex = 0

    /* Split resulting text on full words. */
    if (textBefore.trim() && textBefore.indexOf(' ') >= 0) {
        startIndex = displayText.indexOf(' ')
    }

    return displayText.slice(startIndex, endIndex) + ' ...'
}

function storeSearchResults () {
    const searchbar = document.getElementById('searchbar')
    const query = searchbar.value
    const resultList = document.getElementById('result-list')

    localStorage.setItem('searchQuery', query)
    localStorage.setItem('searchResults', resultList.innerHTML)
}

function loadSearchResults () {
    const searchbar = document.getElementById('searchbar')
    const query = localStorage.getItem('searchQuery')
    const resultList = localStorage.getItem('searchResults')
    const resultsWrapper = document.getElementById('search-results')

    searchbar.value = query
    resultsWrapper.innerHTML = resultList
}

window.addEventListener('DOMContentLoaded', () => {
    loadSearchResults()
})