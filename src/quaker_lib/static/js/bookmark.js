const BOOKMARK_TAG = 'BMCOOK_'
const BOOKMARK_NOTIF = "BMNOTIF";

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
     */
    constructor (id, page, title, paragraph = '') {
        this.id = id

        // The page URL.
        this.page = page

        // The title of the page, for quick display.
        this.title = title
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

    /* Remove "BM_" tag from id */
    const idPath = id.split('_')[1]
    const pageUrl = window.location.pathname + '#' + idPath;
    const bookmark = new Bookmark(id, pageUrl, bookmarkButton.title)
    setCookie(name, JSON.stringify(bookmark))
}

function notificationAccept() {
    const button = document.getElementById('cookie-notification');
    setCookie(BOOKMARK_NOTIF, 1);
    button.style.display = 'none';
}

function checkNotification() {
    const cookie = getCookie(BOOKMARK_NOTIF);

    if (cookie === null) {
        const button = document.getElementById('cookie-notification');
        button.style.display = 'block';
    }
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

function updateBookmark(b, new_title) {
    let cname = bookmarkCookieName(b.id);
    b.title = new_title;
    setCookie(cname, JSON.stringify(b));
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
 * Update bookmark b's title with given new_title.
 * @param {Bookmark} b The bookmark object.
 * @param {string} new_title The new title the bookmark needs to be set to.
 */
function updateBookmark(b, new_title) {
    let cname = bookmarkCookieName(b.id);
    b.title = new_title;
    setCookie(cname, JSON.stringify(b));
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

    const searchbar = document.getElementById('bookmark-searchbar')
    searchbar.focus()
    searchbar.select()

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

    // Clear bookmark searchbar query
    const bookmarkSearchbar = document.getElementById('bookmark-searchbar')
    bookmarkSearchbar.value = '';

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
    } else {
        deleteBookmark(id)
        bookmarkButton.value = 0
    }

    setBookmarkBtn(id);
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
 * Create rename entry when rename button is pressed.
 * @param {string} id The id of the to be deleted bookmark.
 */
function bookmarkRenameClick(id) {
    let bookmark_panel = document.getElementById(`panel-${id}`);
    bookmark_panel.classList.add("edit");

    let bookmark = getBookmark(bookmarkCookieName(id));

    bookmark_panel.innerHTML = createRenameEntry(bookmark);
    inputAddListener(id);
}

/**
 * Add EventListener so Enter key can be pressed to accept new bookmark title.
 * @param {string} id The id of the to be deleted bookmark.
 */
function inputAddListener(id) {
    let inputbox = document.getElementById(`IN_${id}`)
    inputbox.addEventListener("keyup", (e) => {
        if (e.code == 'Enter') {
            renameAccept(id);
        }
    });
    inputbox.focus();
    inputbox.select();
}

/**
 * When accept button is pressed: accept rename by updating bookmark title and
 * reverting innerHTML back to default inner list entry.
 * @param {string} id The id of the to be deleted bookmark.
 */
function renameAccept(id) {
    let bookmark_panel = document.getElementById(`panel-${id}`);
    bookmark_panel.classList.remove("edit");

    let bookmark_old = getBookmark(bookmarkCookieName(id));
    let input_val = document.getElementById(`IN_${id}`).value;
    updateBookmark(bookmark_old, input_val);

    let bookmark_new = getBookmark(bookmarkCookieName(id));
    bookmark_panel.innerHTML = createInnerEntry(bookmark_new);

    // Put renamed bookmark through search filter before new keyup event.
    searchBookmarks();
}

/**
 * When cancel button is pressed: cancel rename by reverting innerHTML back to
 * default inner list entry.
 * @param {string} id The id of the to be deleted bookmark.
 */
function renameCancel(id) {
    let bookmark_panel = document.getElementById(`panel-${id}`);
    bookmark_panel.classList.remove("edit");

    let bookmark = getBookmark(bookmarkCookieName(id));
    bookmark_panel.innerHTML = createInnerEntry(bookmark);
}

/**
 * Render all enabled bookmarks onto the enabled overlay.
 */
 function renderBookmarkList() {
    const bookmarkResults = document.getElementById('bookmark-results')
    const bookmarks = getAllBookmarks()
    let content = '';

    for (const b of bookmarks) {
        content += createBookmarkListEntry(b)
    }

    bookmarkResults.innerHTML = `
                                <table class="table is-hoverable is-fullwidth">
                                <tbody> ${content} </tbody></table>
                                `;
}

/**
 * Create an HTML entry for the given bookmark.
 * @param {*} b The bookmark of which an entry has to be created.
 * @returns {string} The HTML code for the bookmark entry.
 */
 function createBookmarkListEntry(b) {
    let entry = `<tr class="is-fullwidth bookmark-entry" id="panel-${b.id}">
                    ${createInnerEntry(b)}
                </tr>`;
    return entry;
}

/**
 * Create an inner list entry for the given bookmark. This entry appears by
 * default.
 * @param {*} b The bookmark of which an entry has to be created.
 * @returns {string} The HTML code for the bookmark entry.
 */
function createInnerEntry(b) {
    let entry = `
                <td class="icon-table">
                    <i class="fas fa-book" aria-hidden="true"></i>
                </td>
                <td class="title-table"
                onclick="location='${b.page}';hideBookmarkOverlay()">
                    ${b.title}
                </td>
                <td class="button-left-table">
                    <i class="fas fa-pen bookmark-rename"
                    onclick="bookmarkRenameClick('${b.id}')" aria-hidden="true">
                    </i>
                </td>
                <td class="button-right-table">
                    <i class="fas fa-trash bookmark-trash"
                    onclick="bookmarkTrashClick('${b.id}')" aria-hidden="true">
                    </i>
                </td>`;

    return entry;
}

/**
 * Create a rename entry for the given bookmark. This entry appears when the
 * rename button is pressed.
 * @param {*} b The bookmark of which an entry has to be created.
 * @returns {string} The HTML code for the bookmark entry.
 */
function createRenameEntry(b) {
    let entry = `
                <td class="icon-table">
                    <i class="fas fa-pen" aria-hidden="true"></i>
                </td>
                <td class="input-table">
                    <input id="IN_${b.id}" class="input" type="text"
                    value="${b.title}">
                </td>
                <td class="button-left-table">
                    <i class="fa fa-check bookmark-rename"
                    onclick="renameAccept('${b.id}')" aria-hidden="true">
                    </i>
                </td>
                <td class="button-right-table">
                    <i class="fa fa-ban bookmark-trash"
                    onclick="renameCancel('${b.id}')" aria-hidden="true">
                    </i>
                </td>
            `;
    return entry;
}

/**
 * Check if the bookmark button of the given id is activated or not.
 * @param {string} id The id of the to be checked bookmark button.
 * @returns {number} 1 if the button was activated, 0 if not.
 */
function renderBookmarkList () {
    const bookmarkResults = document.getElementById('bookmark-results')
    const bookmarks = getAllBookmarks()
    let content = '';

    let tab = document.createElement('table')
    tab.className = "table is-hoverable is-fullwidth"
    let tbody = document.createElement('tbody')
    tab.appendChild(tbody)

    for (const b of bookmarks) {
        tbody.appendChild(createBookmarkListEntry(b))
    }

    tab.appendChild(tbody)
    bookmarkResults.innerHTML = '';
    bookmarkResults.appendChild(tab);
}

/**
 * Create an HTML entry for the given bookmark.
 * @param {*} b The bookmark of which an entry has to be created.
 * @returns {string} The HTML code for the bookmark entry.
 */
function createBookmarkListEntry(b) {
    var element = document.createElement('tr')
    element.className = "is-fullwidth bookmark-entry"
    element.id = "panel-" + b.id
    element.innerHTML = createInnerEntry(b);

    element.addEventListener('mouseenter', function(event) {
        selectEntry(element, 'bookmark-entry')
    })

    return element;
}

function getBookmarkBtnVal(id) {
    const name = bookmarkCookieName(id)
    if (getBookmark(name) != null) {
        return 1
    }

    return 0
}

/**
 * Toggle (enabled, dark / disabled, blank) the appearance of the bookmark
 * button.
 * @param {*} id The id of the bookmark button which has to be toggled.
 */
function setBookmarkBtn(id) {
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
function loadBookmarks() {
    // Show notification is messaged hasn't been read yet.
    checkNotification();
    const bookmarkButtons = document.getElementsByClassName('bookmark-btn')

    for (const button of bookmarkButtons) {
        setBookmarkBtn(button.id)
    }
}

/**
 * The search function for the bookmarks searchbar
 */
function searchBookmarks() {
    // const items, list, filter, filter
    let item, title, i, txtValue
    const input = document.getElementById('bookmark-searchbar')
    const filter = input.value.toUpperCase()
    /* The results are stored in list and each entry in items. */
    const list = document.getElementById('bookmark-results')
    const items = list.getElementsByClassName('bookmark-entry')

    /* Each bookmark title is collected here and indexed. */
    for (i = 0; i < items.length; i++) {
        title_cell = items[i].getElementsByClassName('title-table');

        /* Ignore if bookmark entry is a rename entry. */
        if (title_cell[0] !== undefined) {
            txtValue = title_cell[0].innerText;

            /* If a title has no index then dont display bookmark,
            * this way you only see needed results.
            */
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                items[i].style.display = '';
            } else {
                items[i].style.display = 'none';
            }
        }
    }
}



// Check bookmark states for buttons on page load.
window.onload = loadBookmarks
