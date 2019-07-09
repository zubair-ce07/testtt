document.getElementById('btn-hello').addEventListener('click', () => {
    let xhr = new XMLHttpRequest()
    xhr.open('POST', 'files/hello.txt', true)
    xhr.onload = function () {
        if (xhr.status == 200) {
            document.getElementById('disp-hello').innerText = xhr.response
            document.getElementById('btn-hello').style.visibility = "hidden"
        }
    }
    xhr.send()
})
