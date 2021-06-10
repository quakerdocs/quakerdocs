document.addEventListener('keydown', (event) => {
    var code = event.code;


    // If user presses Escape and the search bar is open, close the search bar.
    if (code == 'Escape' && searchOpen) {
        hideSearchOverlay();
    }

    // If the user presses 'B', toggle the bookmark overlay.
    if (code == 'KeyB') {
        if (bookmarkOpen) {
            hideBookmarkOverlay();
        } else {
            showBookmarkOverlay();
        }
    }

}, false);