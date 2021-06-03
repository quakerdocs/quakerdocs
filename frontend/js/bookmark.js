/*
        <<< COOKIE SECTION >>>
        If you're looking for bookmark functions, see bookmark section below.
*/
function setCookie(cname, cvalue) {
    let path = "/";
    let date = new Date();
    date.setFullYear(2999);

    document.cookie = `${cname}=${cvalue};expires=${date};path=${path}`
}

function getCookieList() {
    let cookies = decodeURIComponent(document.cookie);
    let clist = cookies.split(';');
    return clist;
}

function getCookie(cname) {
    let clist = getCookieList();
    for (let i = 0; i < clist.length; i++) {
        let name, val;
        [name, val] = clist[i].split('=');

        if (name.trim() === cname.trim()) {
            return val;
        }
    }
    return null;
}

function deleteCookie(cname) {
    if (getCookie(cname) != null) {
        document.cookie = `${cname}=; Max-Age=-99999999;`;
    }
}

/*
        <<< BOOKMARK SECTION >>>
*/

class Bookmark {
    constructor(page, title, paragraph="") {
        // The page URL.
        this.page = page;

        // The title of the page, for quick display.
        this.title = title;

        // Optionally the paragraph title, to allow searching on paragraph level.
        // This is a stretch goal, so it doesn't have to be supported right away.
        this.paragraph = paragraph;
    }
};

function getCurrentName() {
    // Could be changed later if each navigation item has bookmark button.
    return ('bk#' + window.location.pathname).trim();
}

function setBookmark() {
    let cname = getCurrentName();
    let title = document.getElementsByTagName("title")[0].innerHTML;
    // Maybe add preview of page too?
    let bookmark = new Bookmark(window.location.pathname.trim(), title);
    setCookie(cname, JSON.stringify(bookmark));

}

function deleteBookmark() {
    cname = getCurrentName();
    deleteCookie(cname);
}

function getBookmark(cname) {
    let json_bookmark  = getCookie(cname);
    return JSON.parse(json_bookmark);
}

function getAllBookmarks() {
    let bookmarks = []
    let clist = getCookieList();

    console.log(clist);

    for (let i = 0; i < clist.length; i++) {
        let name, val;
        [name, data] = clist[i].split('=');

        if ((name.trim()).substring(0,3) === 'bk#') {
            bookmarks.push(JSON.parse(data))
        }
    }

    return bookmarks;
}

function showBookmarkOverlay() {
    document.getElementById("bookmark-window").classList.add("is-active")

    // Prevent background from scrolling while search window is open.
    document.documentElement.style.overflow = 'hidden';
    document.body.scroll = "no";

    renderBookmarkList();
}

function hideBookmarkOverlay() {
    document.getElementById("bookmark-window").classList.remove("is-active")

    // Allow background to scroll again.
    document.documentElement.style.overflow = 'scroll';
    document.body.scroll = "yes";
}

function renderBookmarkList() {
    let bookmarkResults = document.getElementById("bookmark-results");
    let bookmarks = getAllBookmarks();
    let content = '';

    for (let i = 0; i < bookmarks.length; i++) {
        let b = bookmarks[i]
        content += `<div onclick="location.href='../${b.page}'" class="result"><h1 class="result-title"><strong>
                    ${b.title}</strong></h1></div>`
    }

    bookmarkResults.innerHTML = `<ul>${content}</ul>`;
}