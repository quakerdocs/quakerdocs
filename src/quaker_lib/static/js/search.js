/* Keep track if the WebAssembly module has completed loading. */
let wasm = null
let searcher = null
let searchInput = ""
let searchWords;
let parser = new DOMParser()
let results = []
let scraperProgress = 0
let scraperActive = false
let scraperWordsRegex;
let scraperReplacer;



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
    constructor (page, title, paragraph = "") {
        /* The page URL. */
        this.page = page

        /* The title of the page, for quick display. */
        this.title = title

        /* Optionally the paragraph title, to allow searching on paragraph level. */
        this.paragraph = paragraph

        /* Use the page url as title if necessary. */
        if (!this.title) {
            this.title = this.page.split('.').slice(0, -1).join('.')
        }
    }

    /**
     * Create the html representation of the result
     */
    getHTML () {
        return `<a class="panel-block result is-flex-direction-column" href="${this.page}" onclick="storeSearchResults()">
                <h1 class="result-title"><strong>${this.title}</strong></h1>
                </a>`
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
        const element = document.createElement("div")
        element.className = 'result'
        element.innerHTML = this.getHTML()
        element.addEventListener('mouseenter', function(event) {
            selectEntry(element, 'result')
        })
        return element
    }
}

/**
 * Load and initialise the wasm object that is responsible for the search.
 */
async function initSearchWasm () {
    fetch("./_static/js/search_data.wasm")
        .then(res => res.arrayBuffer())
        .then(buffer => WebAssembly.instantiate(buffer))
        .then(obj => {
            let mem = obj.instance.exports.memory
            let buffer_loc = obj.instance.exports.getIOBuffer()
            let buffer_len = obj.instance.exports.getIOBufferSize()
            obj.instance.search_buffer = new Uint8Array(mem.buffer, buffer_loc, buffer_len)
            wasm = obj.instance
        })
}

initSearchWasm()

/**
 * Perform a search action and yield the results to the HTML page.
 * @param {*} query The query the search should be performed on.
 * @returns {null} Nothing if no results were found.
 * @yields {Result} The next search result entry.
 */
function * performSearch (query) {
    if (wasm == null) {
        return
    }

    /* Upload the string to the wasm. */
    let i, l = Math.min(query.length, wasm.search_buffer.length - 1)
    for (i = 0; i < l; i++)
        wasm.search_buffer[i] = query.charCodeAt(i)
    wasm.search_buffer[i] = 0

    /* Perform the search. */
    wasm.exports.performSearch()

    /* Return the results as they are asked. */
    let decoder = new TextDecoder()
    let len
    while (len = wasm.exports.getSearch()) {
        /* Get the result from the wasm. */
        let result = decoder.decode(wasm.search_buffer.subarray(0, len))
        const sep = result.split('\n')
        yield new Result(sep[0], sep[1], sep[2])
    }
}

/**
 * Callback to update the search whenever a key is pressed.
 * @param event The event that called the callback
 */
function searchUpdateKey (event) {
    const resultsWrapper = document.getElementById('search-results')

    /* Check that the input was changed, if not, do nothing. */
    if (this.value == searchInput)
        return;

    /* Get and store the new input. */
    searchInput = this.value
    scraperProgress = 0
    searchWords = searchInput.split(' ').filter(word => word)
    scraperWordsRegex = searchWords.map(word => new RegExp('\\b' + word, 'ig'))
    let capture = searchWords.map(word => '\\b' + word).join('|')
    scraperReplacer = new RegExp('(' + capture + ')', 'ig')

    results = []

    /* Update the results if there's new input. */
    if (searchInput) {
        searcher = performSearch(searchInput)
        resultsWrapper.innerHTML = '<ul id="result-list"></ul>'
        renderResults()
        selectEntry(document.getElementsByClassName("result")[0], "result");
    } else {
        resultsWrapper.innerHTML = ''
    }
}

/**
 * Callback to add more results to the search when scrolling to the bottom.
 */
function handleInfiniteScroll () {
    if (this.scrollTopMax - this.scrollTop < 90) {
        renderResults(5)
    }
}

/**
 * Add an keyboard event listener to activate a search function
 * {@link performSearch} on every keystroke.
 */
function activateSearch () {
    /* Activate the search bar with an keyboard event listener. */
    const results = document.getElementById('search-results')
    const searchInput = document.getElementById('searchbar')

    if (searchInput) {
        // Update search results when a key is pressed.
        searchInput.addEventListener('keyup', searchUpdateKey)
        results.addEventListener('scroll', handleInfiniteScroll)
    }
}

/**
 * Display the results acquired by the search function {@link performSearch}
 * inside the HTML page alongside some text found in the appropriate pages.
 * @param {*} searcher The generator which yields the search results.
 * @param {*} resultsWrapper The html element in which the results are to be placed.
 */
function renderResults (maxResults = 10) {
    /* Array to store the results into so that the text can be added later. */
    let newResults = Array(maxResults)

    let resultList = document.getElementById('result-list')
    if (resultList == null) {
        return
    }

    for (let index = 0; index < maxResults; index++) {
        /* Limit number of search results. */
        if (searcher == null) {
            return
        }
        let r = searcher.next()
        if (r.done) {
            break
        }

        resultList.append(r.value.createResultElement())
        results.push(r.value)
    }

    /* Link the link elements. */
    let elements = resultList.getElementsByTagName('a')
    for (let i = 0; i < elements.length; i++) {
        results[i].el = elements[i];
    }

    /* Activate the scraper if it is not running yet. */
    if (!scraperActive)
        scraperIterate()
}

/**
 * Start the scraper iterator, which fills the search result textboxes
 * one by one, one after the other.
 */
function scraperIterate () {
    if (scraperProgress >= results.length) {
        scraperActive = false
        return
    }
    scraperActive = true;

    let r = results[scraperProgress++]
    fetch(r.page)
        .then(res => res.text())
        .then(data => {
            const html = parser.parseFromString(data, 'text/html')
            let maxCount = 0, maxSection, maxIndices

            /* Look for the section containing the most words. */
            for (const section of html.querySelectorAll('section')) {
                if (!section.id)
                    continue
                const text = section.textContent;
                let indices = scraperWordsRegex.map(regex => text.search(regex))
                let wordCount = indices.filter(x => x >= 0).length
                if (wordCount > maxCount) {
                    maxCount = wordCount
                    maxSection = section
                    maxIndices = indices
                }
            }

            /* Use the main page of everything no viable section has been found. */
            if (maxCount == 0) {
                maxSection = html.querySelector('main')
                const text = maxSection.textContent;
                maxIndices = scraperWordsRegex.map(regex => text.search(regex))
            }
            else
                r.page += '#' + maxSection.id

            /* Update the html page. */
            r.el.href = r.page
            const start = Math.max(maxIndices[0] - 10, 0)
            let text = maxSection.textContent.substr(start, start + 256)
            text = '...' + text.replace(scraperReplacer,
                '<span class="has-background-primary-light ' +
                'has-text-primary">$1</span>')
            r.el.innerHTML += `<p class="result-content">${text}</p>`

            scraperIterate()
        })
        .catch(console.error)
}

function storeSearchResults () {
    const searchbar = document.getElementById('searchbar')
    const query = searchbar.value
    const resultList = document.getElementById('result-list')
    if (resultList == null) {
        return
    }

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
