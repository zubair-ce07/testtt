document.getElementById('btn-simple').addEventListener('click', () => {
    let xhr = new XMLHttpRequest()
    xhr.open('POST', 'files/lorem1.txt', true)
    xhr.onload = function () {
        if (xhr.status == 200) {
            document.getElementById('disp-simple').innerText = xhr.response
            document.getElementById('btn-simple').style.visibility = "hidden"
        }
    }
    xhr.send()
})
