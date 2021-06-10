document.addEventListener('keydown', (event) => {
    var code = event.code;


    // If user presses Escape and the search bar is open, close the search bar.
    if (code == 'Escape') {
        if (searchOpen) {
            hideSearchOverlay();
        }
        if (bookmarkOpen) {
            hideBookmarkOverlay();
        }
    }

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