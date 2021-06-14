
/**
 * Toggle (show / hide) the sidebar menu on small screens when the hamburger
 * menu button has been clicked.
 */
function toggleMenu() {
    var menu = document.getElementById("menuPanel");

    if (menu.classList.contains('is-hidden-touch')) {
        menu.classList.replace('is-hidden-touch', 'is-full-touch');
    } else {
        menu.classList.replace('is-full-touch', 'is-hidden-touch');
    }
}

/**
 * Expand the element in the sidebar to show its children.
 * @param {Object} element The element to be expanded.
 * @param {Boolean} forceExpand
 */
function toggleExpand(element, forceExpand=false) {
    console.log(element);
    if (element.children.length < 2) {
        return;
    }

    var ul = element.parentElement.getElementsByTagName("UL")[0];
    var i = element.children[1].firstChild.nextSibling;
    if (ul.classList.contains('is-expanded')) {
        if (!forceExpand) {
            i.classList.replace('fa-angle-down', 'fa-angle-right');
            ul.classList.replace('is-expanded', 'is-collapsed');
        }
    } else {
        i.classList.replace('fa-angle-right', 'fa-angle-down');
        ul.classList.replace('is-collapsed', 'is-expanded');
    }
}

let searchOpen = false;

/**
 * Active the overlay containing the search bar and search results.
 */
function showSearchOverlay() {
    document.getElementById("search").classList.add("is-active")
    searchbar = document.getElementById("searchbar")
    searchbar.focus()
    searchbar.select()

    // Prevent background from scrolling while search window is open.
    document.documentElement.style.overflowY = 'hidden';
    document.body.scroll = "no";

    searchOpen = true;
    activateSearch()
}

/**
 * Hide the overlay containing the search bar and results.
 */
function hideSearchOverlay() {
    /* Hide the search bar overlay.
     */
    document.getElementById("search").classList.remove("is-active")

    // Allow background to scroll again.
    document.documentElement.style.overflowY = 'scroll';
    document.body.scroll = "yes";

    searchOpen = false;
}

/**
 * Show or hide the back to top button based on scrolling position.
 */
function toggleBackToTopButton() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        document.getElementById("backTopBtn").style.display = "block";
    } else {
        document.getElementById("backTopBtn").style.display = "none";
    }
}

/**
 * Scroll back to the top of the page.
 */
function backToTop() {
    document.body.scrollTo({top: 0, behavior: 'smooth'}); // For Safari
    document.documentElement.scrollTo({top: 0, behavior: 'smooth'}); // For Chrome, Firefox, IE and Opera
}

/**
 * Expands the sidebar entry of the associated url and it's parents.
 * @param {string} url The url that is associated with the to be expanded
 *     button.
 */
function expandSidebar(url) {
    a = document.querySelector('a[href="' + url + '"]');

    toggleExpand(a.parentElement, forceExpand=true);
    expandULParents(a);
}

/**
 * Expand all the parents of the given element that can be expanded in the
 * sidebar.
 * @param {*} element The element whose parents should be expanded.
 */
function expandULParents(element) {
    console.log(typeof element)
    while (element) {
        if (element.tagName == "UL" &&
            (element.classList.contains("is-collapsed") ||
             element.classList.contains("is-expanded"))) {
            toggleExpand(element.previousSibling, forceExpand=true);
        }
        element = element.parentNode;
    }
}

/**
 * The search function for the bookmarks searchbar
 */
function searchBookmarks() {
    var input, filter, list, items, item, title, i, txtValue;
    input = document.getElementById("bookmark-searchbar");
    filter = input.value.toUpperCase();
    /* The results are stored in list and each entry in items.*/
    list = document.getElementById("bookmark-results");
    items = list.getElementsByClassName("panel-block bookmark-entry");

    /* Each bookmark title is collected here and indexed.*/
    for (i = 0; i < items.length; i++) {
        item = items[i].getElementsByTagName("div");
        title = item[3]
        txtValue = title.innerText;

        /* If a title has no index then dont display  bookmark,
         * this way you only see needed results.
         */
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            items[i].style.display = "";
        } else {
            items[i].style.display = "none";
        }
    }
}

window.onscroll = function() {
    toggleBackToTopButton();
};

document.addEventListener('DOMContentLoaded', function() {
    expandSidebar(document.location.href.split("/").splice(3).join('/'));
}, false);