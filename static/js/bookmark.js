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
        document.cookie = `${cname}=;Max-Age=-99999999;path=/;`
    }
}

/*
        <<< BOOKMARK SECTION >>>
*/

const BOOKMARK_TAG = "bm#";
class Bookmark {
    constructor(id, page, title, paragraph="") {
        this.id = id;

        // The page URL.
        this.page = page;

        // The title of the page, for quick display.
        this.title = title;

        // Optionally the paragraph title, to allow searching on paragraph level.
        // This is a stretch goal, so it doesn't have to be supported right away.
        this.paragraph = paragraph;
    }
};


function bookmarkCookieName(id) {
    return (BOOKMARK_TAG + id).trim();
}

function setBookmark(id) {
    let cname = bookmarkCookieName(id);
    let bookmark_btn = document.getElementById(id);
    let page_url = window.location.pathname + '#' + id.substring(3);
    let bookmark = new Bookmark(id, page_url, bookmark_btn.title);
    setCookie(cname, JSON.stringify(bookmark));

}

function deleteBookmark(id) {
    cname = bookmarkCookieName(id);
    deleteCookie(cname);
}

function getBookmark(cname) {
    let json_bookmark  = getCookie(cname);
    if (json_bookmark != null) {
        return JSON.parse(json_bookmark);
    }
    return null;

}

function getBookmarkBtnVal(id) {
    let cname = bookmarkCookieName(id);
    if (getBookmark(cname) != null) {
        return 1;
    }
    return 0;
}

function getAllBookmarks() {
    let bookmarks = [];
    let clist = getCookieList();

    for (let i = 0; i < clist.length; i++) {
        let name, data;
        [name, data] = clist[i].split('=');

        if ((name.trim()).substring(0,3) === BOOKMARK_TAG) {
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
    // loadBookmarks();
}

function bookmarkClick(id) {
    console.log(id)
    let bookmark_btn = document.getElementById(id);
    if (bookmark_btn.value == 0) {
        setBookmark(id);
        bookmark_btn.value = 1;
        bookmark_btn.innerHTML = '<span class="icon"><i class="fa fa-bookmark"></i></span>';
    } else {
        deleteBookmark(id);
        bookmark_btn.value = 0;
        bookmark_btn.innerHTML = '<span class="icon"><i class="fa fa-bookmark-o"></i></span>';
    }
}

function bookmarkTrashClick(id) {
    console.log(id);
    deleteBookmark(id);
    hideBookmarkOverlay()
    showBookmarkOverlay();
}

function renderBookmarkList() {
    let bookmarkResults = document.getElementById("bookmark-results");
    let bookmarks = getAllBookmarks();
    let content = '';

    for (let i = 0; i < bookmarks.length; i++) {
        let b = bookmarks[i]
        content += createBookmarkListEntry(b);
    }

    bookmarkResults.innerHTML = content;
}

function createBookmarkListEntry(b) {
    let entry = `<div class="panel-block bookmark-entry">
                    <div class="tile is-11" onclick="location='${b.page}';hideBookmarkOverlay()">
                        <div class="level">
                            <div class=level-item>
                                <span class="panel-icon">
                                <i class="fa fa-book" aria-hidden="true"></i>
                                </span>
                            </div>
                            <div class=level-item>
                                ${b.title}
                            </div>
                        </div>
                    </div>
                    <div class="tile is-1">
                        <button class="bookmark-trash" onclick="bookmarkTrashClick('${b.id}')"> <i class="fa fa-trash fa-lg" aria-hidden="true"></i> </button>
                    </div>
                </div>`;
    return entry;
//     `<a class="panel-block" href="${b.page}" onclick="hideBookmarkOverlay()">
//                     <span class="panel-icon">
//                     <i class="fa fa-book" aria-hidden="true"></i>
//                     </span>
//                     ${b.title}
//                 </a>`;
}

function setBookmarkBtn(id) {
    let bookmark_btn = document.getElementById(id);
    bookmark_btn.value = getBookmarkBtnVal(id);

    if (bookmark_btn.value == 0) {
        bookmark_btn.innerHTML = '<span class="icon"><i class="fa fa-bookmark-o"></i></span>';
    } else {
        bookmark_btn.innerHTML = '<span class="icon"><i class="fa fa-bookmark"></i></span>';
    }
}

// function loadBookmarks() {
//     let bookmark_btns = document.getElementsByClassName('bookmark-btn');
//     for (let i = 0; i < bookmark_btns.length; i++) {
//         setBookmarkBtn(bookmark_btns[i].id);
//     }
// }

// Check bookmark states for buttons on page load.
window.onload = () => {
    let bookmark_btns = document.getElementsByClassName('bookmark-btn');
    for (let i = 0; i < bookmark_btns.length; i++) {
        setBookmarkBtn(bookmark_btns[i].id)
    }

}

