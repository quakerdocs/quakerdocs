
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

window.onload = function(e) {
    inject('./pages/checking-for-plagiarism.html', 'div.section', 'div#content')
}
