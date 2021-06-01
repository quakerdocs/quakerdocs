
function inject(filename, element) {
    fetch(filename, {method: 'GET', mode: 'no-cors', credentials: 'same-origin'})
        .then(response => {
            console.log(response)
            console.log(response.ok)
            return response.text()
        })
        .then(data => {
            console.log(data)
            var parser = new DOMParser();
            var htmlDoc = parser.parseFromString(data, 'text/html');
            content = htmlDoc.getElementsByClassName('section')[0].innerHTML
            console.log(content)
            document.querySelector(element).innerHTML = content
        })
        .catch(console.log)
}

window.onload = function(e) {
    console.log("pep")
    inject('./pages/checking-for-plagiarism.html', '#content')
}
