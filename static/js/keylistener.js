document.addEventListener('keydown', (event) => {
    var code = event.code;


    // If user presses Escape and the search bar is open, close the search bar.
    if (code == 'Escape' && searchOpen) {
        hideSearchOverlay();
    }

    // If the user presses 'B', toggle the bookmarks.
    if (code == 'KeyB') {
        bookmarkClick();
    }

}, false);