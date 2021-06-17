
/**
 * Toggle (show / hide) the sidebar menu on small screens when the hamburger
 * menu button has been clicked.
 */
function toggleMenu () {
    const menu = document.getElementById('menuPanel')

    if (menu.classList.contains('is-hidden-touch')) {
        menu.classList.replace('is-hidden-touch', 'is-full-touch')
    } else {
        menu.classList.replace('is-full-touch', 'is-hidden-touch')
    }
}

/**
 * Expand the element in the sidebar to show its children.
 * @param {Object} element The element to be expanded.
 * @param {Boolean} onlyExpand If true, the element will not collapse if it
 *     is expanded, but only expand if it is collapsed.
 */
function toggleExpand (element, onlyExpand = false) {
    if (element.children.length < 2) {
        return
    }

    const ul = element.parentElement.getElementsByTagName('UL')[0]
    const i = element.children[1].firstChild

    if (ul.classList.contains('is-expanded') && !onlyExpand) {
        i.classList.replace('fa-angle-down', 'fa-angle-right')
        ul.classList.replace('is-expanded', 'is-collapsed')
    } else {
        i.classList.replace('fa-angle-right', 'fa-angle-down')
        ul.classList.replace('is-collapsed', 'is-expanded')
    }
}

let searchOpen = false
/**
 * Selects and highlights selected element in the search or bookmark overlay.
 * @param {*} element The element to be highlighted.
 * @param {*} overlay Which overlay the program should look in.
 *     'result' for the search overlay, and 'bookmark-entry' for the bookmark
 *     overlay.
 * @returns {null} If the element was already selected.
 */
function selectEntry(element, overlay) {
    var results = document.getElementsByClassName(overlay + ' selected');

    if (Array.from(results).includes(element)) {
        return null;
    }

    for (var i = 0; i < results.length; i++) {
        results[i].classList.remove('selected');
    }

    element.classList.add('selected');
}

/**
 * Select the element which is offset elements away from the current element.
 * @param {*} offset The offset.
 * @param {*} overlay Which overlay the program should look in.
 *     'result' for the search overlay, and 'bookmark-entry' for the bookmark
 *     overlay.
 * @returns {null} If the element was already selected.
 */
function selectRelativeEntry(offset, overlay) {
    var curEl = document.getElementsByClassName(overlay + ' selected');
    var els = Array.from(document.getElementsByClassName(overlay));
    var index = -1;
    if (curEl.length != 0) {
        index = els.indexOf(curEl[0])
    }

    var newIndex = Math.max(0, Math.min(index + offset, els.length - 1));
    var newEl = document.getElementsByClassName(overlay)[newIndex];

    return selectEntry(newEl, overlay);
}

/**
 * Click the entry to redirect the page to the href of the selected element.
 * @param {*} overlay Which overlay the program should look in.
 *     'result' for the search overlay, and 'bookmark-entry' for the bookmark
 *     overlay.
 * @returns {null} If the element was already selected.
 */
function redirectEntry(overlay) {
    var curEl = document.getElementsByClassName(overlay + ' selected');
    console.log(curEl);
    if (curEl.length == 0) {
        return null;
    }

    if (overlay === 'result') {
        window.location.href = curEl[0].href;
    } else if (overlay === 'bookmark-entry') {
        console.log(curEl[0].children[0])
        console.log(curEl[0].children[0].click());
    }
}

/**
 * Active the overlay containing the search bar and search results.
 */
function showSearchOverlay () {
    document.getElementById('search').classList.add('is-active')
    const searchbar = document.getElementById('searchbar')
    searchbar.focus()
    searchbar.select()

    // Prevent background from scrolling while search window is open.
    document.documentElement.style.overflowY = 'hidden'
    document.body.scroll = 'no'

    searchOpen = true
    activateSearch()
}

/**
 * Hide the overlay containing the search bar and results.
 */
function hideSearchOverlay () {
    /* Hide the search bar overlay.
     */
    document.getElementById('search').classList.remove('is-active')

    // Allow background to scroll again.
    document.documentElement.style.overflowY = 'scroll'
    document.body.scroll = 'yes'

    searchOpen = false
}

/**
 * Show or hide the back to top button based on scrolling position.
 */
function toggleBackToTopButton () {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        document.getElementById('backTopBtn').style.display = 'block'
    } else {
        document.getElementById('backTopBtn').style.display = 'none'
    }
}

/**
 * Scroll back to the top of the page.
 */
function backToTop () {
    // For Safari
    document.body.scrollTo({ top: 0, behavior: 'smooth' })
    // For Chrome, Firefox, IE and Opera
    document.documentElement.scrollTo({ top: 0, behavior: 'smooth' })
}

/**
 * Expands the sidebar entry of the associated url and it's parents.
 * @param {string} url The url that is associated with the to be expanded button.
 */
function expandSidebar (url) {
    const a = document.querySelector('a[href="' + url + '"]')

    toggleExpand(a.parentElement, true)
    expandULParents(a)
}

/**
 * Expand all the parents of the given element that can be expanded in the
 * sidebar.
 * @param {*} element The element whose parents should be expanded.
 */
function expandULParents (element) {
    while (element) {
        if (element.tagName === 'UL' &&
            (element.classList.contains('is-collapsed') ||
            element.classList.contains('is-expanded'))) {
            toggleExpand(element.previousSibling, true)
        }

        element = element.parentNode
    }
}

window.onscroll = () => {
    toggleBackToTopButton()
}

/**
 * When all the content is loaded, call {@link expandSidebar} to expand the
 * current page in the sidebar. Also set the scroll level of the sidebar to be
 * equal to the recorded number.
 */
document.addEventListener('DOMContentLoaded', () => {
    expandSidebar(document.location.href.split('/').splice(3).join('/'))

    const sidebar = document.getElementById('menuPanel')
    sidebar.scrollTo(0, localStorage.getItem('sidebarScrollPos') || 0)

    // Record the current scroll level of the sidebar into a localStorage
    // entry.
    sidebar.onscroll = () => {
        localStorage.setItem('sidebarScrollPos', sidebar.scrollTop)
    }
}, false)
