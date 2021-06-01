
function inject(filename, element) {
    fetch(filename, {method: 'GET', mode: 'no-cors', credentials: 'same-origin'})
        .then(response => {
            return response.text()
        })
        .then(data => {
            var parser = new DOMParser();
            var htmlDoc = parser.parseFromString(data, 'text/html');
            content = htmlDoc.querySelector('div.document').innerHTML
            // navigation = htmlDoc.querySelector('ul.current')
            document.querySelector(element).innerHTML = content
        })
        .catch(console.log)
}

window.onload = function(e) {
    console.log("pep")
    inject('./pages/checking-for-plagiarism.html', '#content')
}
