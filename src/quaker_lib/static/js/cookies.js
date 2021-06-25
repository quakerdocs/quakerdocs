/**
 * Create a new cookie with name=cname and value=cvalue, set to expire in\
 * the year 2999.
 * @param {string} cname The name of the new cookie.
 * @param {*} cvalue The value of the cookie.
 */
function setCookie (cname, cvalue) {
    const path = '/'
    const date = new Date()
    date.setFullYear(2999)

    document.cookie = `${cname}=${cvalue};expires=${date};path=${path};SameSite=Lax;`
}

/**
 * Retrieve all cookies from the website.
 * @returns {Array} Array of all cookies.
 */
function getCookieList () {
    const cookies = decodeURIComponent(document.cookie)
    return cookies.split(';')
}

/**
 * Get the value of the cookie with name=cname.
 * @param {string} cname The name of the to be retrieved cookie.
 * @returns {*} The value of the cookie or null if the cookie wasn't found.
 */
function getCookie (name) {
    const cList = getCookieList()

    for (const cookie of cList) {
        const [name2, val] = cookie.split('=')

        if (name.trim() === name2.trim()) {
            return val
        }
    }

    return null
}

/**
 * Delete the cookie with name=cname.
 * @param {string} cname The name of the to be deleted cookie.
 */
function deleteCookie (name) {
    if (getCookie(name) != null) {
        setCookie(name, '')
    }
}
