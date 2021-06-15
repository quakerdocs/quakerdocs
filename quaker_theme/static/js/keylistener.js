document.addEventListener('keyup', (event) => {
    var code = event.code;

    /**
     * If user presses Escape and the search bar is open, close the search
     * overlay or bookmark overlay.
     */
    if (code == 'Escape') {
        if (searchOpen) {
            hideSearchOverlay();
        }
        if (bookmarkOpen) {
            hideBookmarkOverlay();
        }
    }

    // If any overlay is open, do not allow any other overlay to open.
    var anyOpen = searchOpen || bookmarkOpen;

    if (anyOpen)
        return;

    // If the user presses 'S', toggle the search overlay.
    if (code == 'KeyS') {
        if (!searchOpen) {
            showSearchOverlay();
        }
    }

    // If the user presses 'B', toggle the bookmark overlay.
    if (code == 'KeyB') {
        if (!bookmarkOpen) {
            showBookmarkOverlay()
        }
    }
}, false);