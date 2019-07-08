document.getElementById('btn-hello').addEventListener('click', () => {
    let xhr = new XMLHttpRequest()
    xhr.open('GET', 'files/hello.txt', true)
    xhr.onload = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            document.getElementById('disp-hello').innerText = xhr.responseText
            document.getElementById('btn-hello').style.visibility = "hidden"
        }
    }
    xhr.send()
})
