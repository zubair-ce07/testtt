var countryElement = document.getElementById("countrySelector"),
    languageElement = document.getElementById("languageSelector"),
    criteriaElement = document.getElementById("criteriaSelector"),
    usersToShow = 20

document.getElementById("argumentHandler").addEventListener("change", (event) => {
    if(checkAllFieldsAreFilled()) {
        fetchUsers(countryElement.value, languageElement.value, criteriaElement.value)
    }
})

function checkAllFieldsAreFilled() {
    return (languageElement.value != "" && criteriaElement.value != "" && countryElement.value != "") ? true : false;
}

function fetchUsers(country, language, criteria) {
    let clientRequest = new XMLHttpRequest()
    let query = `https://api.github.com/search/users?o=desc&q=language%3A${encodeURIComponent(language)}+location%3A${country}&sort=${criteria}&type=users&usersToShow=${usersToShow}`

    clientRequest.open("GET", query, true)
    clientRequest.responseType = "json"

    clientRequest.onload = function () {
        if (clientRequest.status == 200) {

            // remove nodes from last request
            var displayNode = document.getElementById("disp");
            displayNode.style.visibility = "visible"
            while (displayNode.firstChild) {
                displayNode.removeChild(displayNode.firstChild);
            }
            displayNode.style = ""

            // create heading to show on top on cards jumbotron
            let heading = document.createElement("h2");
            heading.style.textAlign = "center"
            heading.style.paddingBottom = "50px"
            heading.innerHTML = `By ${criteria.toUpperCase()}: Top ${usersToShow}/${clientRequest.response["total_count"]} users in <u>${country.toUpperCase()}</u>, who work in <i>${language.toUpperCase()}</i>`
            displayNode.appendChild(heading)


            // make all the cards from received JSON
            let cards = []
            clientRequest.response["items"].forEach((singleUser, index) => {
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

            
            // end of results marker
            let endText = document.createElement("h4");
            endText.style.textAlign = "center"
            endText.innerText = `... End of Results ...`
            endText.style.marginTop = "50px"
            displayNode.appendChild(endText)
        }
    }
    clientRequest.send()
}

// returns a single card
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
