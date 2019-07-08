document.getElementById('submit').addEventListener('click', () => {
    let file = document.getElementById('form').value
    let xhr = new XMLHttpRequest()
    xhr.open('GET', 'files/' + file, true)
    xhr.onload = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            document.getElementById('disp-form').innerText = xhr.responseText
            // document.getElementById('btn-form').style.visibility = "hidden"
        }
    }
    xhr.send()
})
