const COUNTRY_ELEMENT = document.getElementById("countrySelector"),
      LANGUAGE_ELEMENT = document.getElementById("languageSelector"),
      CRITERIA_ELEMENT = document.getElementById("criteriaSelector"),
      NUMBER_OF_USERS_DISPLAYED = 20,
      API_BASE_URL = "https://api.github.com/",
      ASYNC_API_CALL = true,
      API_REQUEST_SUCCESSFUL = 200,
      REQ_METHOD = "GET",
      RES_TYPE = "json"


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

        // remove nodes from last request
        var displayNode = document.getElementById("disp");
        while (displayNode.firstChild) {
            displayNode.removeChild(displayNode.firstChild);
        }

        makeElementVisible(displayNode);
        
        // create heading to show on top on cards jumbotron
        let heading = createHTMLElement("h2", 
                                        {"textAlign": "center", "paddingBottom": "50px"}, 
                                        `By ${CRITERIA_ELEMENT.value.toUpperCase()}: Top 
                                         ${NUMBER_OF_USERS_DISPLAYED}/${this.response["total_count"]} 
                                         users in <u>${COUNTRY_ELEMENT.value.toUpperCase()}</u>, who work in 
                                         <i>${LANGUAGE_ELEMENT.value.toUpperCase()}</i>`)
        displayNode.appendChild(heading)

        // make all the cards from received JSON
        let cards = []
        this.response["items"].forEach((singleUser, index) => {
            let login = singleUser["login"],
                id = singleUser["id"],
                avatar_url = singleUser["avatar_url"],
                github_url = singleUser["html_url"],
                api_url = singleUser["url"]
            
            let userCard = document.createElement("div");
            userCard.innerHTML = createCard(index + 1, login, id, avatar_url, github_url, api_url);
            cards.push(userCard)
        })


        // make rows of 4 cards each and siplay on screen
        for(let i = 0; i < cards.length - cards.length % 4; i = i + 4) {
            let cardDeck = document.createElement("div");
            cardDeck.className = "card-deck"
            cardDeck.innerHTML = cards[i].innerHTML + cards[i+1].innerHTML + cards[i+2].innerHTML + cards[i+3].innerHTML
            displayNode.appendChild(cardDeck)
        }
        
        // handle the remaining less than 4 cards for last row
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
            default:
                console.log(cards.length % 4)
        }
        displayNode.appendChild(lastDeck)

        let endText = createHTMLElement("h4", 
                                        {"textAlign": "center", "marginTop": "50px"},
                                        `... End of Results ...`)
        displayNode.appendChild(endText)
    }
}
