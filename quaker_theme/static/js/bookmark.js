const BOOKMARK_TAG = 'BMCOOK_'

/**
 * Class representing the necessary bookmark data.
 */
class Bookmark {
    /**
     * Create a new bookmark instance.
     * @constructor
     * @param {*} id The id of the bookmark.
     * @param {*} page The page URL where the bookmark belongs to.
     * @param {*} title The title of the page where the bookmark belongs to.
     * @param {*} paragraph TODO: Define paragraph.
     */
    constructor (id, page, title, paragraph = '') {
        this.id = id

        // The page URL.
        this.page = page

        // The title of the page, for quick display.
        this.title = title

        // Optionally the paragraph title, to allow searching on paragraph
        // level. This is a stretch goal, so it doesn't have to be supported
        // right away.
        this.paragraph = paragraph
    }
}

/**
 * Create a new cookie name for the bookmarks using the given id.
 * @param {string} id The id of the to be bookmarked page.
 * @returns {string} The cookie name that should be used.
 */
function bookmarkCookieName (id) {
    return (BOOKMARK_TAG + id).trim()
}

/**
 * Create a new bookmark and cookie with the given id.
 * @param {string} id The id to create the bookmark with.
 */
function setBookmark (id) {
    const name = bookmarkCookieName(id)
    const bookmarkButton = document.getElementById(id)

    /* substring(3), because id starts with BM_ */
    const pageUrl = window.location.pathname + '#' + id.substring(3)
    const bookmark = new Bookmark(id, pageUrl, bookmarkButton.title)
    setCookie(name, JSON.stringify(bookmark))
}

/**
 * Delete the bookmark and cookie with the given id.
 * @param {string} id The id of the bookmark and cookie to be deleted.
 */
function deleteBookmark (id) {
    cname = bookmarkCookieName(id)
    deleteCookie(cname)
}

/**
 * Get the data bookmark with the given cname.
 * @param {string} cname The name of the to be retrieved bookmark.
 * @returns {*} The data contained in the bookmark cookie.
 */
function getBookmark (cname) {
    const cookie = getCookie(cname)
    if (cookie) {
        return JSON.parse(cookie)
    }

    return null
}

/**
 * Check if the bookmark button of the given id is activated or not.
 * @param {string} id The id of the to be checked bookmark button.
 * @returns {number} 1 if the button was activated, 0 if not.
 */
function getBookmarkBtnVal (id) {
    const name = bookmarkCookieName(id)
    if (getBookmark(name) != null) {
        return 1
    }

    return 0
}

/**
 * Retrieve all pages which have enabled bookmark.
 * @returns {Array} The array of enabled bookmark pages.
 */
function getAllBookmarks () {
    const bookmarks = []
    const cList = getCookieList()

    for (const cookie of cList) {
        const [name, data] = cookie.split('=')

        if ((name.trim()).startsWith(BOOKMARK_TAG)) {
            if (data) {
                bookmarks.push(JSON.parse(data))
            }
        }
    }

    return bookmarks
}

let bookmarkOpen = false

/**
 * Show the overlay with the enabled bookmarks on it.
 */
function showBookmarkOverlay () {
    document.getElementById('bookmark-window').classList.add('is-active')

    bookmarkOpen = true

    // Prevent background from scrolling while search window is open.
    document.documentElement.style.overflowY = 'hidden'
    document.body.scroll = 'no'

    renderBookmarkList()
}

/**
 * Hide the overlay with the enabled bookmarks on it.
 */
function hideBookmarkOverlay () {
    document.getElementById('bookmark-window').classList.remove('is-active')

    bookmarkOpen = false
    // Allow background to scroll again.
    document.documentElement.style.overflowY = 'scroll'
    document.body.scroll = 'yes'

    loadBookmarks()
}

/**
 * Toggle (enable / disable) the bookmark function when a bookmark button is
 * clicked.
 * @param {string} id The id of the to be toggled bookmark.
 */
function bookmarkClick (id) {
    const bookmarkButton = document.getElementById(id)
    if (bookmarkButton.value == 0) {
        setBookmark(id)
        bookmarkButton.value = 1
        bookmarkButton.innerHTML = '<span class="icon"><i class="fa \
                                    fa-bookmark"></i></span>'
    } else {
        deleteBookmark(id)
        bookmarkButton.value = 0
        bookmarkButton.innerHTML = '<span class="icon"><i class="fa \
                                    fa-bookmark-o"></i></span>'
    }
}

/**
 * Delete the bookmark if the trash bin button on the bookmark overlay was
 * clicked.
 * @param {string} id The id of the to be deleted bookmark.
 */
function bookmarkTrashClick (id) {
    deleteBookmark(id)
    const bookmarkPanel = document.getElementById(`panel-${id}`)
    bookmarkPanel.style.display = 'none'
}

/**
 * Render all enabled bookmarks onto the enabled overlay.
 */
function renderBookmarkList () {
    const bookmarkResults = document.getElementById('bookmark-results')
    const bookmarks = getAllBookmarks()
    let content = ''

    for (const b of bookmarks) {
        content += createBookmarkListEntry(b)
    }

    bookmarkResults.innerHTML = content
}

/**
 * Create an HTML entry for the given bookmark.
 * @param {*} b The bookmark of which an entry has to be created.
 * @returns {string} The HTML code for the bookmark entry.
 */
function createBookmarkListEntry (b) {
    let title = b.title
    const titleWords = title.split(' ')
    const maxWords = 12

    /* Cut off title if it is too long. */
    if (titleWords.length > maxWords) {
        title = titleWords.slice(0, maxWords).join(' ') + '...'
    }

    return `<div id="panel-${b.id}" class="panel-block bookmark-entry" onmouseover="selectEntry(this, 'bookmark-entry')">
                <div class="tile is-11" onclick="location='${b.page}'; \
                hideBookmarkOverlay()">
                    <div class="level">
                        <div class=level-item>
                            <span class="panel-icon">
                            <i class="fa fa-book" aria-hidden="true"></i>
                            </span>
                        </div>
                        <div class=level-item>
                            ${title}
                        </div>
                    </div>
                </div>
                <div class="tile is-1">
                    <button class="bookmark-trash" onclick=" \
                    bookmarkTrashClick('${b.id}')"><i class="fa fa-trash \
                    fa-lg" aria-hidden="true"></i></button>
                </div>
            </div>`
}

/**
 * Toggle (enabled, dark / disabled, blank) the appearance of the bookmark
 * button.
 * @param {*} id The id of the bookmark button which has to be toggled.
 */
function setBookmarkBtn (id) {
    const bookmarkButton = document.getElementById(id)
    bookmarkButton.value = getBookmarkBtnVal(id)

    if (bookmarkButton.value == 0) {
        bookmarkButton.innerHTML = '<span class="icon"><i class="fa \
                                    fa-bookmark-o"></i></span>'
    } else {
        bookmarkButton.innerHTML = '<span class="icon"><i class="fa \
                                    fa-bookmark"></i></span>'
    }
}

/**
 * Load the values of the bookmark buttons when the page had just loaded.
 */
function loadBookmarks () {
    const bookmarkButtons = document.getElementsByClassName('bookmark-btn')

    for (const button of bookmarkButtons) {
        setBookmarkBtn(button.id)
    }
}

/**
 * The search function for the bookmarks searchbar
 */
function searchBookmarks () {
    // const items, list, filter, filter
    let item, title, i, txtValue
    const input = document.getElementById('bookmark-searchbar')
    const filter = input.value.toUpperCase()
    /* The results are stored in list and each entry in items. */
    const list = document.getElementById('bookmark-results')
    const items = list.getElementsByClassName('panel-block bookmark-entry')

    /* Each bookmark title is collected here and indexed. */
    for (i = 0; i < items.length; i++) {
        item = items[i].getElementsByTagName('div')
        title = item[3]
        txtValue = title.innerText

        /* If a title has no index then dont display  bookmark,
         * this way you only see needed results.
         */
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            items[i].style.display = ''
        } else {
            items[i].style.display = 'none'
        }
    }
}

// Check bookmark states for buttons on page load.
window.onload = loadBookmarks
