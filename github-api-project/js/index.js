const COUNTRY_ELEMENT = document.getElementById("countrySelector"),
      LANGUAGE_ELEMENT = document.getElementById("languageSelector"),
      CRITERIA_ELEMENT = document.getElementById("criteriaSelector"),
      NUMBER_OF_USERS_DISPLAYED = 20,
      API_BASE_URL = "https://api.github.com/",
      ASYNC_API_CALL = true,
      API_REQUEST_SUCCESSFUL = 200,
      REQ_METHOD = "GET",
      RES_TYPE = "json",
      USER_CARDS_PER_ROW = 4,
      EMPTY_STRING = ""


function validateGithubAPIArgs() {
    return (LANGUAGE_ELEMENT.value != EMPTY_STRING && CRITERIA_ELEMENT.value != EMPTY_STRING && COUNTRY_ELEMENT.value != EMPTY_STRING) ? ASYNC_API_CALL : false;
}


function createHTMLElement(elementType, elementStyleInfo, elementInnerHTML) {
    let newElement = document.createElement(elementType);

    for(eachAttribute in elementStyleInfo){
        let attributeValue = elementStyleInfo[eachAttribute]
        newElement.style[eachAttribute] = attributeValue;
    }

    newElement.innerHTML = elementInnerHTML;

    return newElement;
}


function removeCustomStyle(displayElement) {
    displayElement.style = EMPTY_STRING;
}


document.getElementById("argumentHandler").addEventListener("change", (event) => {
    if(validateGithubAPIArgs()) {
        fetchUsers(COUNTRY_ELEMENT.value, LANGUAGE_ELEMENT.value, CRITERIA_ELEMENT.value)
    }
})


function createOneUserCard(number, username, id, avatar_url, github_url) {
    let userCard = document.createElement('div')
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


function githubAPICaller(query, onloadFunction) {
    let clientRequest = new XMLHttpRequest()

    clientRequest.open(REQ_METHOD, query, ASYNC_API_CALL)
    clientRequest.responseType = RES_TYPE
    clientRequest.onload = onloadFunction;
    clientRequest.send()
}


function fetchUsers(country, language, criteria) {
    const QUERY = `${API_BASE_URL}search/users?o=desc&q=language%3A${encodeURIComponent(language)}+location%3A${country}&sort=${criteria}&type=users&per_page=${NUMBER_OF_USERS_DISPLAYED}`

    githubAPICaller(QUERY, userInfoOnLoad)
}

function removeAllChildren(elementID) {
    var mainDisplayElement = document.getElementById(elementID);
    while (mainDisplayElement.firstChild) {
        mainDisplayElement.removeChild(mainDisplayElement.firstChild);
    }
}


function userInfoOnLoad() {
    if (this.status == API_REQUEST_SUCCESSFUL) {
        const API_RESPONSE = this.response
        let userCards = []

        removeAllChildren("disp")
        removeCustomStyle(mainDisplayElement);
        
        let heading = createHTMLElement("h2", 
                                        {"textAlign": "center", "paddingBottom": "50px"}, 
                                        `By ${CRITERIA_ELEMENT.value.toUpperCase()}: Top 
                                         ${NUMBER_OF_USERS_DISPLAYED}/${API_RESPONSE["total_count"]} 
                                         users in <u>${COUNTRY_ELEMENT.value.toUpperCase()}</u>, who work in 
                                         <i>${LANGUAGE_ELEMENT.value.toUpperCase()}</i>`)
        mainDisplayElement.appendChild(heading)
        
        API_RESPONSE["items"].forEach((singleUser, index) => {
            let username = singleUser["login"],
                id = singleUser["id"],
                avatarURL = singleUser["avatar_url"],
                githubURL = singleUser["html_url"],
                apiURL = singleUser["url"]

            userCards.push(createOneUserCard(index + 1, username, id, avatarURL, githubURL, apiURL))
        })

        for(let i = 0; i < userCards.length; i = i + USER_CARDS_PER_ROW) {
            let cardDeck = document.createElement("div");
            cardDeck.className = "card-deck"

            let remainingCards = i + USER_CARDS_PER_ROW <= userCards.length ? USER_CARDS_PER_ROW : userCards.length % USER_CARDS_PER_ROW

            for(let j = i; j < i + remainingCards; j++) {
                cardDeck.appendChild(userCards[j])
            }
            mainDisplayElement.appendChild(cardDeck)
        }

        let endText = createHTMLElement("h4", 
                                        {"textAlign": "center", "marginTop": "50px"},
                                        `... End of Results ...`)
        mainDisplayElement.appendChild(endText)
    }
}
