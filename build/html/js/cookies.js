/**
 * Create a new cookie with name=cname and value=cvalue, set to expire in\
 * the year 2999.
 * @param {string} cname The name of the new cookie.
 * @param {*} cvalue The value of the cookie.
 */
function setCookie(cname, cvalue) {
    let path = "/";
    let date = new Date();
    date.setFullYear(2999);

    document.cookie = `${cname}=${cvalue};expires=${date};path=${path};SameSite=Lax;Secure`;
}

/**
 * Retrieve all cookies from the website.
 * @returns {Array} Array of all cookies.
 */
function getCookieList() {
    let cookies = decodeURIComponent(document.cookie);
    let clist = cookies.split(';');
    return clist;
}

/**
 * Get the value of the cookie with name=cname.
 * @param {string} cname The name of the to be retrieved cookie.
 * @returns {*} The value of the cookie or null if the cookie wasn't found.
 */
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

/**
 * Delete the cookie with name=cname.
 * @param {string} cname The name of the to be deleted cookie.
 */
function deleteCookie(cname) {
    if (getCookie(cname) != null) {
        setCookie(cname, "");
    }
}
