
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
 * @param {*} element The element to be expanded.
 */
function toggleExpand(element) {
    var ul = element.parentElement.parentElement.getElementsByTagName("UL")[0];
    var i = element.firstChild.nextSibling;

    if (ul.classList.contains('is-expanded')) {
        i.classList.replace('fa-angle-down', 'fa-angle-right');
        ul.classList.replace('is-expanded', 'is-collapsed');
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
    document.documentElement.style.overflow = 'hidden';
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
    document.documentElement.style.overflow = 'scroll';
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
 * Expand the corresponding navigation menu entry in the sidebar.
 */
function expandSidebar() {
    // TODO
    return;
}

window.onscroll = function() {
    toggleBackToTopButton();
};

window.onload = function() {
    expandSidebar();
};
