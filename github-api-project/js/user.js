const NUMBER_OF_USERS_DISPLAYED = 12,
      API_BASE_URL = "https://api.github.com/",
      ASYNC_API_CALL = true,
      API_REQUEST_SUCCESSFUL = 200,
      REQ_METHOD = "GET",
      USERNAME = new URL(window.location).searchParams.get("login"),
      USER_CARDS_PER_ROW = 4,
      REPO_CARDS_PER_ROW = 2,
      TABBED_PROFILE_ELEMENT = document.getElementById("user-profile-page"),
      HOME_TAB = "#home",
      FOLLOWERS_TAB = "#followers",
      FOLLOWING_TAB = "#following",
      REPOS_TAB = "#repositories",
      JSON_NULL = "-",
      EMPTY_STRING = "",
      RES_TYPE = "json",
      USER_API_RESP_STRUCT = {
        username: "login",
        githubID: "id",
        avatarURL: "avatar_url",
        githubURL: "html_url",
        fullName: "name",
        location: "location",
        company: "company",
        bio: "bio",
        blogURL: "blog",
        followersURL: "followers",
        followingURL: "following",
        reposURL: "public_repos",
        joinedAt: "created_at"
      },
      REPO_API_RESP_STRUCT = {
        fullName: "name",
        description: "description",
        created: "created_at",
        updated: "updated_at",
        watchers: "watchers_count",
        language: "language",
        forks: "forks_count",
        issues: "open_issues_count",
        license: "license",
        directURL: "html_url",
      }

let previousTab = null

if(USERNAME != null){
    document.getElementById("username").innerText = USERNAME
    fetchUser()
}


TABBED_PROFILE_ELEMENT.addEventListener("click", (event) => {
    const targetTab = event.target.getAttribute("href")

    if(previousTab != targetTab && targetTab != null) {
        let tabIdWithoutHashTag = targetTab.split("#")[1]
        emptyTab(tabIdWithoutHashTag)
        previousTab = targetTab

        if(targetTab == HOME_TAB) {
            fetchUser()
        } else if(targetTab == FOLLOWERS_TAB) {
            fetchFollowers()
        } else if(targetTab == FOLLOWING_TAB) {
            fetchFollowing()
        } else if(targetTab == REPOS_TAB) {
            fetchRepos()
        }
    }
})


function githubAPICaller(query) {
    return new Promise(function(resolve, reject){
        let clientRequest = new XMLHttpRequest()

        clientRequest.open(REQ_METHOD, query, ASYNC_API_CALL)
        clientRequest.responseType = RES_TYPE
        clientRequest.onload = function() {
            if (clientRequest.status == API_REQUEST_SUCCESSFUL) {
                resolve(clientRequest.response)
            } else {
                reject(new Error('Failed 200 OK => API Request was not Successful!'))
            }
        };
        clientRequest.send()
    })
}


function fetchUser(){
    const QUERY = `${API_BASE_URL}users/${USERNAME}`
    githubAPICaller(QUERY).then((returnedJsonData)=> {
        onloadUserInfo(returnedJsonData)
    })
}


function fetchFollowers() {
    let QUERY = `${API_BASE_URL}users/${USERNAME}/followers?per_page=${NUMBER_OF_USERS_DISPLAYED}`
    githubAPICaller(QUERY).then((returnedJsonData)=> {
        onloadUserFollowers(returnedJsonData)
    })
}


function fetchFollowing() {
    let QUERY = `${API_BASE_URL}users/${USERNAME}/following?per_page=${NUMBER_OF_USERS_DISPLAYED}`
    githubAPICaller(QUERY).then((returnedJsonData)=> {
        onloadUserFollowing(returnedJsonData)
    })
}


function fetchRepos() {
    let QUERY = `${API_BASE_URL}users/${USERNAME}/repos?per_page=${NUMBER_OF_USERS_DISPLAYED}`
    githubAPICaller(QUERY).then((returnedJsonData)=> {
        onloadUserRepos(returnedJsonData)
    })
}


function onloadUserInfo(userInfo) {
    let userJoinedDate = new Date(userInfo[USER_API_RESP_STRUCT.joinedAt]);

    modifyHTMLElement("avatar", "src", userInfo[USER_API_RESP_STRUCT.avatarURL])
    modifyHTMLElement("github-url", "href", userInfo[USER_API_RESP_STRUCT.githubURL])
    modifyHTMLElement("github-url", "target", "__blank")
    modifyHTMLElement("real-name", "innerText", userInfo[USER_API_RESP_STRUCT.fullName])
    modifyHTMLElement("user-location", "innerText", userInfo[USER_API_RESP_STRUCT.location] ? userInfo[USER_API_RESP_STRUCT.location] : JSON_NULL)
    modifyHTMLElement("user-company", "innerText", userInfo[USER_API_RESP_STRUCT.company] ? userInfo[USER_API_RESP_STRUCT.company] : JSON_NULL)
    modifyHTMLElement("user-bio", "innerText", userInfo[USER_API_RESP_STRUCT.bio] ? userInfo[USER_API_RESP_STRUCT.bio] : EMPTY_STRING)
    modifyHTMLElement("user-joined", "innerText", `${userJoinedDate.getDay()}/${userJoinedDate.getMonth()}/${userJoinedDate.getFullYear()}`)
    modifyHTMLElement("user-blog", "innerHTML", userInfo[USER_API_RESP_STRUCT.blogURL] ? formatUserBlogInfo(userInfo[USER_API_RESP_STRUCT.blogURL]) : JSON_NULL)
    modifyHTMLElement("user-followers-badge", "innerText", userInfo[USER_API_RESP_STRUCT.followersURL])
    modifyHTMLElement("user-following-badge", "innerText", userInfo[USER_API_RESP_STRUCT.followingURL])
    modifyHTMLElement("user-repos-badge", "innerText", userInfo[USER_API_RESP_STRUCT.reposURL])
}


function onloadUserFollowers(returnedJsonData) {
    let mainDisplayElement = document.getElementById("display-followers");
    displayUsers(mainDisplayElement, returnedJsonData)

    fixButtonHref("display-followers-button", "followers")
}


function onloadUserFollowing(returnedJsonData) {
    let mainDisplayElement = document.getElementById("display-following");
    displayUsers(mainDisplayElement, returnedJsonData)

    fixButtonHref("display-following-button", "following")
}


function onloadUserRepos(returnedJsonData) {
    let mainDisplayElement = document.getElementById("display-repositories");
    let repoCardsList = []

    returnedJsonData.forEach((repo) => {
        userCard = createOneRepoCard(repo[REPO_API_RESP_STRUCT.fullName],
                                    repo[REPO_API_RESP_STRUCT.description] ? repo[REPO_API_RESP_STRUCT.description] : spanNullValue("No Description Available", "warning"),
                                    new Date(repo[REPO_API_RESP_STRUCT.created]).toDateString(),
                                    new Date(repo[REPO_API_RESP_STRUCT.updated]).toDateString(),
                                    repo[REPO_API_RESP_STRUCT.watchers],
                                    repo[REPO_API_RESP_STRUCT.language] ? repo[REPO_API_RESP_STRUCT.language] : spanNullValue("Unknown", "danger"),
                                    repo[REPO_API_RESP_STRUCT.forks],
                                    repo[REPO_API_RESP_STRUCT.issues],
                                    repo[REPO_API_RESP_STRUCT.license] ? repo[REPO_API_RESP_STRUCT.license]["name"] : spanNullValue("Unknown", "danger"),
                                    repo[REPO_API_RESP_STRUCT.directURL]);

        repoCardsList.push(userCard)
    })

    for(let i = 0; i < repoCardsList.length; i = i + REPO_CARDS_PER_ROW) {
        let cardDeck = document.createElement("div");
        cardDeck.className = "card-deck"
        let remainingCards = i + REPO_CARDS_PER_ROW <= repoCardsList.length ? REPO_CARDS_PER_ROW : repoCardsList.length % REPO_CARDS_PER_ROW
        for(let j = i; j < i + remainingCards; j++) {
            cardDeck.appendChild(repoCardsList[j])
        }
        mainDisplayElement.appendChild(cardDeck)
    }

    fixButtonHref("display-repositories-button", EMPTY_STRING)
}


function fixButtonHref(buttonID, githubPage) {
    document.getElementById(buttonID).href = `https://github.com/${USERNAME}/${githubPage}`;
    document.getElementById(buttonID).target = "__blank";
}


function emptyTab(tabID) {
    if(tabID != "home") {
        var tabElement = document.getElementById("display-" + tabID);

        while (tabElement.firstChild) {
            tabElement.removeChild(tabElement.firstChild);
        }
    }
}


function modifyHTMLElement(elementID, elementAttribute, newValue) {
    document.getElementById(elementID)[elementAttribute] = newValue
}


function formatUserBlogInfo(userBlog){
    return `<a target="__blank" href=${userBlog}> ${userBlog} </a>`
}


function spanNullValue(nullReplacer, className) {
    return `<span class="bg-${className} text-center"> ${nullReplacer} </span>`
}


function displayUsers(mainDisplayElement, apiCallResult) {
    let userCards = []

    apiCallResult.forEach((singleUser, index) => {
        userCards.push(createOneUserCard(index + 1, singleUser[USER_API_RESP_STRUCT.username], singleUser[USER_API_RESP_STRUCT.githubID], singleUser[USER_API_RESP_STRUCT.avatarURL], singleUser[USER_API_RESP_STRUCT.githubURL]))
    })

    for(let i = 0; i < userCards.length; i = i + USER_CARDS_PER_ROW) {
        let cardDeck = document.createElement("div");
        let remainingCards = i + USER_CARDS_PER_ROW <= userCards.length ? USER_CARDS_PER_ROW : userCards.length % USER_CARDS_PER_ROW
        cardDeck.className = "card-deck"

        for(let j = i; j < i + remainingCards; j++) {
            cardDeck.appendChild(userCards[j])
        }

        mainDisplayElement.appendChild(cardDeck)
    }
}


function createOneUserCard(number, username, id, avatar_url, github_url) {
    let userCard = document.createElement("div")
    userCard.className= "card text-white bg-secondary mb-3 border-success"
    userCard.style = "width: 18rem;"

    userCard.innerHTML = `<div class="card-header text-bold">${number}</div>
                            <img class="card-img-top" src="${avatar_url}" alt="Card image cap">

                            <div class="card-body">
                                <h5 class="card-title text-center">${username}</h5>
                            </div>

                            <div class="card-footer bg-secondary text-center">
                                <a href="user.html?login=${username}" class="btn btn-success">View Profile</a>
                            </div>
                        </div>`
    return userCard
}


function createOneRepoCard(repoName, repoDescription, repoCreated, repoUpdated, repoWatchers, repoLanguage, repoForks, repoIssuesCount, repoLicense, repoURL){
    let repoCard = document.createElement("div")
    repoCard.className= "card text-white bg-secondary mb-3 border-success"
    repoCard.style = "width: 18rem;"
    
    repoCard.innerHTML =    `<div class="card-header text-center">
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
                        </div>`
    return repoCard
}
