document.getElementById('btn-simple').addEventListener('click', () => {
    let xhr = new XMLHttpRequest()
    xhr.open('GET', 'files/random.txt', true)
    xhr.onload = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            document.getElementById('disp-simple').innerText = xhr.responseText
            document.getElementById('btn-simple').style.visibility = "hidden"
        }
    }
    xhr.send()
})
