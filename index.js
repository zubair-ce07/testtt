function createCard(login, id, avatar_url, github_url) {
    return `<div class="card" style="width: 18rem;">
            <img class="card-img-top" src="${avatar_url}" alt="Card image cap">
            <div class="card-body">
                <h5 class="card-title">${id + ": " + login}</h5>
                <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
                <a href="${github_url}" class="btn btn-primary">Visit on Github</a>
            </div>
            </div>`
}

let users = []

function sendRequest(since) {
    if(since < 100000){
        let xhr = new XMLHttpRequest()
        xhr.open('GET', 'https://api.github.com/users?per_page=100&since=' + since, true)
        xhr.responseType = 'json'
        xhr.onload = function () {
            if (xhr.status == 200) {
                for (let singleUser in xhr.response){
                    let login = xhr.response[singleUser]['login'],
                        id = xhr.response[singleUser]['id'],
                        avatar_url = xhr.response[singleUser]['avatar_url'],
                        github_url = xhr.response[singleUser]['html_url']

                    let userCard = document.createElement('div');
                    userCard.innerHTML = createCard(login, id, avatar_url, github_url);
                    document.getElementById('disp').appendChild(userCard)
                }
                since += xhr.response.length
                console.log(since)
                // sendRequest(since)
            }
        }
        xhr.send()
    }
}

sendRequest(0);

