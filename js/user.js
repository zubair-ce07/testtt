var username = new URL(window.location).searchParams.get("login")
console.log(username)




// document.getElementById('argumentHandler').addEventListener('change', (event) => {
//     if(language_element.value != 'None' && criteria_element.value != 'None') {
//         fetchUsers(country_element.value, language_element.value, criteria_element.value)
//     }
// })

function fetchUsers(country, language, criteria) {
    let clientRequest = new XMLHttpRequest()
    let query = `https://api.github.com/search/users?q=language%3A${language}+location%3A${country}&s=${criteria}&type=users&per_page=${per_page}`
    // console.log(query)
    clientRequest.open('GET', query, true)
    clientRequest.responseType = 'json'
    clientRequest.onload = function () {
        if (clientRequest.status == 200) {

            var displayNode = document.getElementById("disp");
            displayNode.style.visibility = 'visible'
            while (displayNode.firstChild) {
                displayNode.removeChild(displayNode.firstChild);
            }

            let heading = document.createElement('h2');
            heading.style.textAlign = 'center'
            heading.style.paddingBottom = '50px'
            heading.innerText = `Top ${per_page} users in ${country.toUpperCase()}, who work in ${language.toUpperCase()}`
            displayNode.appendChild(heading)

            let cards = []

            for (let singleUser in clientRequest.response['items']){
                let login = clientRequest.response['items'][singleUser]['login'],
                    id = clientRequest.response['items'][singleUser]['id'],
                    avatar_url = clientRequest.response['items'][singleUser]['avatar_url'],
                    github_url = clientRequest.response['items'][singleUser]['html_url'],
                    api_url = clientRequest.response['items'][singleUser]['url']
                
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
                default:
                    console.log(cards.length % 4)
            }

            displayNode.appendChild(lastDeck)

            let endText = document.createElement('h4');
            endText.style.textAlign = 'center'
            // endText.style.paddingBottom = '20px'
            endText.innerText = `... End of Results ...`
            endText.style.marginTop = '50px'
            displayNode.appendChild(endText)
        }
    }

    clientRequest.send()
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
