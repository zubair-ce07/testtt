const COUNTRY_ELEMENT = document.getElementById("countrySelector"),
      LANGUAGE_ELEMENT = document.getElementById("languageSelector"),
      CRITERIA_ELEMENT = document.getElementById("criteriaSelector"),
      NUMBER_OF_USERS_DISPLAYED = 20,
      API_BASE_URL = "https://api.github.com/",
      ASYNC_API_CALL = true,
      API_REQUEST_SUCCESSFUL = 200,
      REQ_METHOD = "GET",
      RES_TYPE = "json",
      USER_CARDS_PER_ROW = 4


function validateGithubAPIArgs() {
    return (LANGUAGE_ELEMENT.value != "" && CRITERIA_ELEMENT.value != "" && COUNTRY_ELEMENT.value != "") ? ASYNC_API_CALL : false;
}


function createHTMLElement(elementType, elementStyleInfo, elementInnerHTML) {
    let newElement = document.createElement(elementType);

    for(each in elementStyleInfo){
        newElement.style[each] = elementStyleInfo[each];
    }

    newElement.innerHTML = elementInnerHTML;

    return newElement;
}


function makeElementVisible(displayElement) {
    displayElement.style = "";
}


document.getElementById("argumentHandler").addEventListener("change", (event) => {
    if(validateGithubAPIArgs()) {
        fetchUsers(COUNTRY_ELEMENT.value, LANGUAGE_ELEMENT.value, CRITERIA_ELEMENT.value)
    }
})


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


function fetchUsers(country, language, criteria) {
    const QUERY = `${API_BASE_URL}search/users?o=desc&q=language%3A${encodeURIComponent(language)}+location%3A${country}&sort=${criteria}&type=users&per_page=${NUMBER_OF_USERS_DISPLAYED}`
    
    let clientRequest = new XMLHttpRequest()

    clientRequest.responseType = RES_TYPE
    clientRequest.open(REQ_METHOD, QUERY, ASYNC_API_CALL)
    clientRequest.onload = onloadFunc

    
    clientRequest.send()
}


function onloadFunc() {
    if (this.status == API_REQUEST_SUCCESSFUL) {

        var mainDisplayElement = document.getElementById("disp");

        while (mainDisplayElement.firstChild) {
            mainDisplayElement.removeChild(mainDisplayElement.firstChild);
        }

        makeElementVisible(mainDisplayElement);
        
        let heading = createHTMLElement("h2", 
                                        {"textAlign": "center", "paddingBottom": "50px"}, 
                                        `By ${CRITERIA_ELEMENT.value.toUpperCase()}: Top 
                                         ${NUMBER_OF_USERS_DISPLAYED}/${this.response["total_count"]} 
                                         users in <u>${COUNTRY_ELEMENT.value.toUpperCase()}</u>, who work in 
                                         <i>${LANGUAGE_ELEMENT.value.toUpperCase()}</i>`)
        mainDisplayElement.appendChild(heading)

        let cards = []
        this.response["items"].forEach((singleUser, index) => {
            let login = singleUser["login"],
                id = singleUser["id"],
                avatarURL = singleUser["avatar_url"],
                githubURL = singleUser["html_url"],
                apiURL = singleUser["url"]
            
            let userCard = document.createElement("div");
            userCard.innerHTML = createCard(index + 1, login, id, avatarURL, githubURL, apiURL);
            cards.push(userCard)
        })


        // make rows of USER_CARDS_PER_ROW cards each and siplay on screen
        for(let i = 0; i < cards.length; i = i + USER_CARDS_PER_ROW) {
            let cardDeck = document.createElement("div");
            cardDeck.className = "card-deck"
            let remainingCards = i + USER_CARDS_PER_ROW <= cards.length ? USER_CARDS_PER_ROW : cards.length % USER_CARDS_PER_ROW
            for(let j = i; j < i + remainingCards; j++) {
                cardDeck.innerHTML += cards[j].innerHTML
            }
            mainDisplayElement.appendChild(cardDeck)
        }

        let endText = createHTMLElement("h4", 
                                        {"textAlign": "center", "marginTop": "50px"},
                                        `... End of Results ...`)
        mainDisplayElement.appendChild(endText)
    }
}
