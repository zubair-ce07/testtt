var username = new URL(window.location).searchParams.get("login")
document.getElementById("username").innerText = username
var per_page = 8

if(username != null){
    fetchUser(username)
}


document.getElementById('user-profile-page').addEventListener('click', (event) => {
    if(event.target.getAttribute('href') == '#home') {
        fetchUser(username)
    } else if(event.target.getAttribute('href') == '#followers') {
        fetchFollowers(username)
    } else if(event.target.getAttribute('href') == '#following') {
        fetchFollowing(username)
    } else if(event.target.getAttribute('href') == '#repositories') {
        fetchRepos(username)
    }
})


function fetchUser(username){
    let query = `https://api.github.com/users/${username}`
    let clientRequest = new XMLHttpRequest()
    clientRequest.open('GET', query, true)
    clientRequest.responseType = 'json'
    clientRequest.onload = function () {
        if (clientRequest.status == 200) {

            document.getElementById("avatar").src = clientRequest.response['avatar_url']
            document.getElementById("github-url").href = clientRequest.response['html_url']
            document.getElementById("github-url").target = '__blank'
            document.getElementById("real-name").innerText = clientRequest.response['name']
            document.getElementById("user-location").innerText = clientRequest.response['location'] ? clientRequest.response['location'] : "-"
            document.getElementById("user-company").innerText = clientRequest.response['company'] ? clientRequest.response['company'] : "-"
            document.getElementById("user-bio").innerText = clientRequest.response['bio'] ? clientRequest.response['bio'] : ""
            var date = new Date(clientRequest.response['created_at']);
            document.getElementById("user-joined").innerText = `${date.getDay()}/${date.getMonth()}/${date.getFullYear()}`
            document.getElementById("user-blog").innerHTML = clientRequest.response['blog'] ? `<a target="__blank" href=${clientRequest.response['blog']}> ${clientRequest.response['blog']} </a>` : "-"
            document.getElementById("user-followers-badge").innerText = clientRequest.response['followers']
            document.getElementById("user-following-badge").innerText = clientRequest.response['following']
            document.getElementById("user-repos-badge").innerText = clientRequest.response['public_repos']
        }
    }

    clientRequest.send()
}

function fetchFollowers(username) {
    let query = `https://api.github.com/users/${username}/followers?per_page=${per_page}`
    let clientRequest = new XMLHttpRequest()
    clientRequest.open('GET', query, true)
    clientRequest.responseType = 'json'
    clientRequest.onload = function () {
        if (clientRequest.status == 200) {
            let displayNode = document.getElementById("display-followers");
            displayUsers(displayNode, username, clientRequest.response)
        }

        document.getElementById('display-followers-button').href = `https://github.com/${username}/followers`
        document.getElementById('display-followers-button').target = '__blank'
    }
    clientRequest.send()
}

function fetchFollowing(username) {
    let query = `https://api.github.com/users/${username}/following?per_page=${per_page}`
    let clientRequest = new XMLHttpRequest()
    clientRequest.open('GET', query, true)
    clientRequest.responseType = 'json'
    clientRequest.onload = function () {
        if (clientRequest.status == 200) {

            let displayNode = document.getElementById("display-following");
            displayUsers(displayNode, username, clientRequest.response)
        }

        document.getElementById('display-following-button').href = `https://github.com/${username}/following`
        document.getElementById('display-following-button').target = '__blank'
    }
    
    clientRequest.send()
}


function fetchRepos(username) {
    let query = `https://api.github.com/users/${username}/repos?per_page=${per_page}`
    let clientRequest = new XMLHttpRequest()
    clientRequest.open('GET', query, true)
    clientRequest.responseType = 'json'
    clientRequest.onload = function () {
        if (clientRequest.status == 200) {
            let displayNode = document.getElementById("display-repositories");
            let cards = []

            for (let oneRepo in clientRequest.response) {
                let repoName = clientRequest.response[oneRepo]['name'],
                    repoFullName = clientRequest.response[oneRepo]['full_name'],
                    repoURL = clientRequest.response[oneRepo]['html_url'],
                    repoDescription = clientRequest.response[oneRepo]['description'] ? clientRequest.response[oneRepo]['description'] : '<span class="text-warning text-center"> No Description Available </span>',
                    repoCreated = new Date(clientRequest.response[oneRepo]['created_at']).toDateString(),
                    repoUpdated = new Date(clientRequest.response[oneRepo]['updated_at']).toDateString(),
                    repoWatchers = clientRequest.response[oneRepo]['watchers_count'],
                    repoLanguage = clientRequest.response[oneRepo]['language'],
                    repoForks = clientRequest.response[oneRepo]['forks_count']
                    repoIssuesCount = clientRequest.response[oneRepo]['open_issues_count']
                    repoLicense = clientRequest.response[oneRepo]["license"] ? clientRequest.response[oneRepo]["license"]['name'] : "unknown"
                
                let userCard = document.createElement('div');
                userCard.innerHTML = createRepoCard(repoName, repoDescription, repoCreated, repoUpdated, repoWatchers, repoLanguage, repoForks, repoIssuesCount, repoLicense, repoURL);
                cards.push(userCard)
            }

            for(let i = 0; i < cards.length - cards.length % 2; i = i + 2) {
                let cardDeck = document.createElement('div');
                cardDeck.className = 'card-deck'
                cardDeck.innerHTML = cards[i].innerHTML + cards[i+1].innerHTML
                displayNode.appendChild(cardDeck)
            }
            
            var lastDeck = document.createElement('div');
            lastDeck.className = 'card-deck'

            switch(cards.length % 2) {
                case 1:
                    lastDeck.innerHTML = cards[cards.length - cards.length % 2].innerHTML
                    break;
            }    

            displayNode.appendChild(lastDeck)
        }

        document.getElementById('display-repositories-button').href = `https://github.com/${username}/`
        document.getElementById('display-repositories-button').target = '__blank'
    }
    clientRequest.send()
}

function displayUsers(displayNode, username, api_call_result) {
    let cards = []

    for (let singleUser in api_call_result) {
        let login = api_call_result[singleUser]['login'],
            id = api_call_result[singleUser]['id'],
            avatar_url = api_call_result[singleUser]['avatar_url'],
            github_url = api_call_result[singleUser]['html_url'],
            api_url = api_call_result[singleUser]['url']
        
        let userCard = document.createElement('div');
        userCard.innerHTML = createCard(+singleUser+1, login, id, avatar_url, github_url, api_url);
        cards.push(userCard)
    }

    for(let i = 0; i < cards.length - cards.length % 4; i = i + 4) {
        let cardDeck = document.createElement('div');
        cardDeck.className = 'card-deck'
        cardDeck.innerHTML = cards[i].innerHTML + cards[i+1].innerHTML + cards[i+2].innerHTML + cards[i+3].innerHTML
        displayNode.appendChild(cardDeck)
    }
    
    var lastDeck = document.createElement('div');
    lastDeck.className = 'card-deck'

    switch(cards.length % 4) {
        case 1:
            lastDeck.innerHTML = cards[cards.length - cards.length % 4].innerHTML
            break;
        case 2:
            lastDeck.innerHTML = cards[cards.length - cards.length % 4].innerHTML + cards[cards.length - cards.length % 4 + 1].innerHTML
            break;
        case 3:
            lastDeck.innerHTML = cards[cards.length - cards.length % 4].innerHTML + cards[cards.length - cards.length % 4 + 1].innerHTML + cards[cards.length - cards.length % 4 + 2].innerHTML
            break;
    }    

    displayNode.appendChild(lastDeck)
}

function createCard(number, login, id, avatar_url, github_url) {
    return `<div class="card text-white bg-secondary mb-3 border-success" style="width: 18rem;">
            <div class="card-header text-bold">${number}</div>
            <img class="card-img-top" src="${avatar_url}" alt="Card image cap">
            <div class="card-body">
                <h5 class="card-title text-center">${login}</h5>
            </div>
            <div class="card-footer bg-secondary text-center">
                <a href="user.html?login=${login}" class="btn btn-success">View Profile</a>
            </div>
            </div>`
}

function createRepoCard(repoName, repoDescription, repoCreated, repoUpdated, repoWatchers, repoLanguage, repoForks, repoIssuesCount, repoLicense, repoURL){
    return `<div class="card text-white bg-secondary mb-3 border-success" style="width: 18rem;">

            <div class="card-header text-center">
                <div class="row">
                    <div class="col-sm">
                        <p class="text-center font-weight-bold"> ${repoName} </p> 
                    </div>
                    <div class="col-sm text-right my-auto">
                        <a href="${repoURL}" target="__blank" class="btn btn-primary">View on Github</a>
                    </div>
                </div>
                <p>Language: ${repoLanguage} </p> 
                <p> License: ${repoLicense} </p>
            </div>

            <div class="card-body">
                <p> ${repoDescription} </p>
            </div>

            <div class="card-footer bg-secondary text-center">
                <p class="bg-danger p-1 medium"> Created at: ${repoCreated} </p>
                <p class="bg-info p-1"> Last Updated: <br> ${repoUpdated} </p>
            </div>
            
            <div class="card-footer bg-secondary medium">
                <div class="row text-center">
                    <div class="col-sm bg-primary">
                    Watchers: ${repoWatchers}
                    </div>
                    <div class="col-sm bg-warning">
                    Forks: ${repoForks}
                    </div>
                    <div class="col-sm bg-danger">
                    Issues: ${repoIssuesCount}
                    </div>
                </div>
            </div>
            </div>`
}
