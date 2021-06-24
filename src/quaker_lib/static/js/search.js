/* Keep track if the WebAssembly module has completed loading. */
let wasm = null
let searcher = null
let searchInput = ""
let parser = new DOMParser()

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
 * TODO
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


function searchUpdateKey (event) {
    const resultsWrapper = document.getElementById('search-results')
    const code = event.code

    // Don't execute a new search when any arrow key or enter is pressed.
    if (['ArrowDown', 'ArrowUp', 'ArrowLeft', 'ArrowRight', 'Enter'].includes(code)) {
        return
    }

    searchInput = this.value

    if (searchInput) {
        searcher = performSearch(searchInput)
        resultsWrapper.innerHTML = '<ul id="result-list"></ul>'
        renderResults()
        selectEntry(document.getElementsByClassName("result")[0], "result");
    } else {
        resultsWrapper.innerHTML = ''
    }
}

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

    let index = 0

    for (; index < maxResults; index++) {
        /* Limit number of search results. */
        if (searcher == null) {
            return
        }
        let r = searcher.next()
        if (r.done) {
            break
        }

        resultList.append(r.value.createResultElement())
        newResults[index] = r.value
    }

    resultList = resultList.getElementsByTagName("a")
    let i = 0
    const input = searchInput

    // let words = input.split(/[ ]+/)
    // let wordsRegex =
    // new RegExp(query, 'i')

    function getContent() {
        if (i >= index) {
            return
        }

        let r = newResults[i]
        fetch(r.page)
            .then(res => res.text())
            .then(data => {
                if (input != searchInput) {
                    return
                }

                const html = parser.parseFromString(data, 'text/html')
                let text = html.getElementById('content').innerText

                /* Look for the section containing the result. */
                for (const section of html.querySelectorAll('section')) {
                    if (section.textContent.includes(searchInput) && section.id) {
                        r.page += '#' + section.id
                        text = section.innerText
                        break
                    }
                }

                /* TODO: highlight each word in the input separately. */
                let content = highlightSearchQuery(searchInput, text)
                console.log(resultList[resultList.length - index + i])
                resultList[resultList.length - index + i].href = r.page
                resultList[resultList.length - index + i].innerHTML += `<p class="result-content">${content}</p>`

                i++
                getContent()
            })
            .catch(console.error)
    }

    /* Fetch page contents. */
    getContent()
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
