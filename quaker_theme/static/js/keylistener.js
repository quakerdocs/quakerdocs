document.addEventListener('keyup', (event) => {
    const code = event.code;

    /**
     * If user presses Escape and the search bar is open, close the search
     * overlay or bookmark overlay.
     */
    if (code === 'Escape') {
        if (searchOpen) {
            hideSearchOverlay()
        }

        if (bookmarkOpen) {
            hideBookmarkOverlay()
        }
    }

    if (searchOpen) {
        if (code === 'ArrowDown') {
            selectRelativeEntry(1, 'result');
        } else if (code === 'ArrowUp') {
            selectRelativeEntry(-1, 'result');
        } else if (code === 'Enter') {
            redirectEntry('result');
        }
    } else if (bookmarkOpen) {
        if (code === 'ArrowDown') {
            selectRelativeEntry(1, 'bookmark-entry');
        } else if (code === 'ArrowUp') {
            selectRelativeEntry(-1, 'bookmark-entry');
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
