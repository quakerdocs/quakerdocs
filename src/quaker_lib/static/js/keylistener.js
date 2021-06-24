document.addEventListener('keydown', (event) => {
    const code = event.code;

    if (document.getElementsByClassName('bookmark-entry edit').length != 0) {
        return;
    }
    /**
     * If user presses Escape and the search overlay or bookmark overlay
     *  is open, close the search overlay or bookmark overlay.
     */
    if (code === 'Escape') {
        if (searchOpen) {
            hideSearchOverlay()
        }

        if (bookmarkOpen) {
            hideBookmarkOverlay()
        }
    }

    /**
     * Keyboard controls for search and bookmark overlays:
     * Arrow Up or Arrow Down: Select the next or previous entry respectively.
     * Enter: 'Click' on the currently selected entry.
     */
    if (searchOpen) {
        if (code === 'ArrowDown') {
            selectRelativeEntry('result', true);
        } else if (code === 'ArrowUp') {
            selectRelativeEntry('result', false);
        } else if (code === 'Enter') {
            redirectEntry('result');
            storeSearchResults();
        }
    } else if (bookmarkOpen) {
        if (code === 'ArrowDown') {
            selectRelativeEntry('bookmark-entry', true);
        } else if (code === 'ArrowUp') {
            selectRelativeEntry('bookmark-entry', false);
        } else if (code === 'Enter') {
            redirectEntry('bookmark-entry');
        }
    } else {
        // If any overlay is open, do not allow any other overlay to open.
        // If the user presses 'S', toggle the search overlay.
        if (code === 'KeyS') {
            if (!searchOpen) {
                showSearchOverlay()
            }
        }

        // If the user presses 'B', toggle the bookmark overlay.
        if (code === 'KeyB') {
            if (!bookmarkOpen) {
                showBookmarkOverlay()
            }
        }
    }
}, false)
