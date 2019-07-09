document.getElementById('submit').addEventListener('click', () => {
    let file = document.getElementById('form').value
    let xhr = new XMLHttpRequest()
    xhr.open('GET', 'files/' + file, true)
    xhr.onload = function () {
        if (xhr.status == 200) {
            if(file.split('.')[1] == 'json') {
                document.getElementById('disp-form-json').innerHTML = JSON.stringify(xhr.response, undefined, 2)
                document.getElementById('disp-form').innerText = ""
            } else {
                document.getElementById('disp-form').innerText = xhr.responseText
                document.getElementById('disp-form-json').innerHTML = ""
            }
            
        }
    }
    if(file.split('.')[1] == 'json') {
        xhr.responseType = 'json'
    }
    xhr.send()
})
