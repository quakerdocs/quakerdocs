function setCookie(cname, cvalue) {
    let path = "/";
    let date = new Date();
    date.setFullYear(2999);

    document.cookie = `${cname}=${cvalue};${date};${path}`
}

function getAllCookies() {
    let cookies = decodeURIComponent(document.cookie);
    let clist = cookies.split(';');
    return clist;
}

function checkCookie(cname) {
    let clist = getAllCookies();
    for (let i = 0; i < clist.length; i++) {
        let name, val;
        [name, val] = clist[i].split('=');
        console.log([name, cname]);
        if (name.trim() === cname.trim()) {
            return true;
        }
    }
    return false;
}

function deleteCookie(cname) {
    if (checkCookie(cname)) {
        document.cookie = `${cname}=; Max-Age=-99999999;`;
    }
}

function getBookmarkName() {
    // Could be changed later if each navigation item has bookmark button.
    return window.location.pathname.trim();
}

function setBookmark() {
    cname = getBookmarkName();
    setCookie(cname, 1);

}

function deleteBookmark() {
    console.log('testse')
    cname = getBookmarkName();
    deleteCookie(cname);
}
