function inject(filename, src_element, dst_element) {
    fetch(filename, {method: 'GET', mode: 'no-cors', credentials: 'same-origin'})
        .then(res => res.text())
        .then(data => {
            var parser = new DOMParser()
            var htmlDoc = parser.parseFromString(data, 'text/html')
            content = htmlDoc.querySelector(src_element).innerHTML
            document.querySelector(dst_element).innerHTML = content
        })
        .catch(console.log)
}

// window.onload = function(e) {
//     inject('./pages/checking-for-plagiarism.html', 'div.section', 'div#content')
// }

// Used to toggle the menu on small screens when clicking on the menu button
function toggleFunction() {
    var x = document.getElementById("mini-menu");
    if (x.className.indexOf("hide") == -1) {
        x.className = x.className.replace("", "hide");
    } else {
        x.className = x.className.replace("hide", "");
    }
}

function overlayOn() {
    document.getElementById("overlay").style.display = "block";
}

function overlayOff() {
    document.getElementById("overlay").style.display = "none";
}