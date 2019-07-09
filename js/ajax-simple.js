document.getElementById('btn-simple').addEventListener('click', () => {
    let xhr = new XMLHttpRequest()
    xhr.open('GET', 'files/lorem1.txt', true)
    xhr.onload = function () {
        if (xhr.status == 200) {
            document.getElementById('disp-simple').innerText = xhr.responseText
            document.getElementById('btn-simple').style.visibility = "hidden"
        }
    }
    xhr.send()
})
