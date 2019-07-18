const NUMBER_OF_USERS_DISPLAYED = 8,
      API_BASE_URL = "https://api.github.com/",
      ASYNC_API_CALL = true,
      API_REQUEST_SUCCESSFUL = 200,
      REQ_METHOD = "GET",
      USERNAME = new URL(window.location).searchParams.get("login");
      



function fixButtonHref(buttonID, githubPage) {
    document.getElementById(buttonID).href = `https://github.com/${USERNAME}/${githubPage}`;
    document.getElementById(buttonID).target = "__blank";
}


if(USERNAME != null){
    document.getElementById("username").innerText = USERNAME
    fetchUser()
}


// event listener for different tabs
document.getElementById("user-profile-page").addEventListener("click", (event) => {
    if(event.target.getAttribute("href") == "#home") {
        fetchUser()
    } else if(event.target.getAttribute("href") == "#followers") {
        fetchFollowers()
    } else if(event.target.getAttribute("href") == "#following") {
        fetchFollowing()
    } else if(event.target.getAttribute("href") == "#repositories") {
        fetchRepos()
    }
})

function modifyHTMLElement(elementID, elementAttribute, newValue) {
    document.getElementById(elementID)[elementAttribute] = newValue
}

function onloadUserInfo() {
    let userInfo = this.response,
        userJoinedDate = new Date(userInfo["created_at"]);

    if (this.status == API_REQUEST_SUCCESSFUL) {
        modifyHTMLElement("avatar", "src", userInfo["avatar_url"])
        modifyHTMLElement("github-url", "href", userInfo["html_url"])
        modifyHTMLElement("github-url", "target", "__blank")
        modifyHTMLElement("real-name", "innerText", userInfo["name"])
        modifyHTMLElement("user-location", "innerText", userInfo["location"] ? userInfo["location"] : "-")
        modifyHTMLElement("user-company", "innerText", userInfo["company"] ? userInfo["company"] : "-")
        modifyHTMLElement("user-bio", "innerText", userInfo["bio"] ? userInfo["bio"] : "")
        modifyHTMLElement("user-joined", "innerText", `${userJoinedDate.getDay()}/${userJoinedDate.getMonth()}/${userJoinedDate.getFullYear()}`)
        modifyHTMLElement("user-blog", "innerHTML", userInfo["blog"] ? `<a target="__blank" href=${userInfo["blog"]}> ${userInfo["blog"]} </a>` : "-")
        modifyHTMLElement("user-followers-badge", "innerText", userInfo["followers"])
        modifyHTMLElement("user-following-badge", "innerText", userInfo["following"])
        modifyHTMLElement("user-repos-badge", "innerText", userInfo["public_repos"])
    }
}


function onloadUserFollowers() {
    if (this.status == API_REQUEST_SUCCESSFUL) {
        let displayNode = document.getElementById("display-followers");
        displayUsers(displayNode, this.response)
    }

    fixButtonHref("display-followers-button", "followers")
}


function onloadUserFollowing() {
    if (this.status == API_REQUEST_SUCCESSFUL) {

        let displayNode = document.getElementById("display-following");
        displayUsers(displayNode, this.response)
    }

    fixButtonHref("display-following-button", "following")
}


function onloadUserRepos() {
    if (this.status == API_REQUEST_SUCCESSFUL) {

        let displayNode = document.getElementById("display-repositories");
        let repoCardsList = []

        this.response.forEach((repo) => {
            let userCard = document.createElement("div");
            userCard.innerHTML = createRepoCard(repo["name"],
                                                repo["description"] ? repo["description"] : "<span class='text-warning text-center'> No Description Available </span>",
                                                new Date(repo["created_at"]).toDateString(),
                                                new Date(repo["updated_at"]).toDateString(),
                                                repo["watchers_count"],
                                                repo["language"] ? repo["language"] : `<span class="bg-danger"> unknown </span>`,
                                                repo["forks_count"],
                                                repo["open_issues_count"],
                                                repo["license"] ? repo["license"]["name"] : `<span class="bg-danger"> unknown </span>`,
                                                repo["html_url"]);
                                                repoCardsList.push(userCard)
        })

        for(let i = 0; i < repoCardsList.length - repoCardsList.length % 2; i = i + 2) {
            let cardDeck = document.createElement("div");
            cardDeck.className = "card-deck"
            cardDeck.innerHTML = repoCardsList[i].innerHTML + repoCardsList[i+1].innerHTML
            displayNode.appendChild(cardDeck)
        }
        
        var lastDeck = document.createElement("div");
        lastDeck.className = "card-deck"

        switch(repoCardsList.length % 2) {
            case 1:
                lastDeck.innerHTML = repoCardsList[repoCardsList.length - repoCardsList.length % 2].innerHTML
                break;
        }    

        displayNode.appendChild(lastDeck)
    }

    fixButtonHref("display-repositories-button", "")
}


function fetchUser(){
    const QUERY = `${API_BASE_URL}users/${USERNAME}`
    console.log(QUERY)

    let clientRequest = new XMLHttpRequest()

    clientRequest.open(REQ_METHOD, QUERY, ASYNC_API_CALL)
    clientRequest.responseType = "json"
    clientRequest.onload = onloadUserInfo;

    clientRequest.send()
}


function fetchFollowers() {
    let QUERY = `${API_BASE_URL}users/${USERNAME}/followers?per_page=${NUMBER_OF_USERS_DISPLAYED}`

    let clientRequest = new XMLHttpRequest()

    clientRequest.responseType = "json"
    clientRequest.onload = onloadUserFollowers

    clientRequest.open(REQ_METHOD, QUERY, ASYNC_API_CALL)
    clientRequest.send()
}


function fetchFollowing() {
    let QUERY = `${API_BASE_URL}users/${USERNAME}/following?per_page=${NUMBER_OF_USERS_DISPLAYED}`

    let clientRequest = new XMLHttpRequest()

    clientRequest.responseType = "json"
    clientRequest.onload = onloadUserFollowing
    
    clientRequest.open(REQ_METHOD, QUERY, ASYNC_API_CALL)
    clientRequest.send()
}


function fetchRepos() {
    let QUERY = `${API_BASE_URL}users/${USERNAME}/repos?per_page=${NUMBER_OF_USERS_DISPLAYED}`
    
    let clientRequest = new XMLHttpRequest()

    clientRequest.responseType = "json"
    clientRequest.onload = onloadUserRepos

    clientRequest.open(REQ_METHOD, QUERY, ASYNC_API_CALL)
    clientRequest.send()
}


// displays followers/following profiles in cards
function displayUsers(displayNode, apiCallResult) {
    let cards = []

    apiCallResult.forEach((singleUser, index) => {
        let login = singleUser["login"],
            id = singleUser["id"],
            avatarURL = singleUser["avatar_url"],
            githubURL = singleUser["html_url"],
            apiURL = singleUser["url"]
        
        let userCard = document.createElement("div");
        userCard.innerHTML = createUserCard(index + 1, login, id, avatarURL, githubURL, apiURL);
        cards.push(userCard)
    })

    for(let i = 0; i < cards.length - cards.length % 4; i = i + 4) {
        let cardDeck = document.createElement("div");
        cardDeck.className = "card-deck"
        cardDeck.innerHTML = cards[i].innerHTML + cards[i+1].innerHTML + cards[i+2].innerHTML + cards[i+3].innerHTML
        displayNode.appendChild(cardDeck)
    }
    
    var lastDeck = document.createElement("div");
    lastDeck.className = "card-deck"

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


function createUserCard(number, login, id, avatarURL, githubURL) {
    return `<div class="card text-white bg-secondary mb-3 border-success" style="width: 18rem;">
                <div class="card-header text-bold">${number}</div>

                <img class="card-img-top" src="${avatarURL}" alt="Card image cap">

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
                    <p> Language: ${repoLanguage} </p> 
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
