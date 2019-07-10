var country_element = document.getElementById('countrySelector'),
    language_element = document.getElementById('languageSelector'),
    criteria_element = document.getElementById('criteriaSelector')

document.getElementById('argumentHandler').addEventListener('change', (event) => {
    // if(event.target == country_element) {
    //     console.log(country_element.value)
    // } else if (event.target == language_element) {
    //     console.log(language_element.value)
    // } else if (event.target == criteria_element) {
    //     console.log(criteria_element.value)
    // }

    if(language_element.value != 'None' && criteria_element.value != 'None') {
        fetchUsers(country_element.value, language_element.value, criteria_element.value)
    }
    
})

function fetchUsers(country, language, criteria) {
    let clientRequest = new XMLHttpRequest()
    let query = `https://api.github.com/search/users?q=language%3A${language}+location%3A${country}&s=${criteria}&type=users&per_page=20`
    console.log(query)
    clientRequest.open('GET', query, true)
    clientRequest.responseType = 'json'
    clientRequest.onload = function () {
        if (clientRequest.status == 200) {

            var displayNode = document.getElementById("disp");
            while (displayNode.firstChild) {
                displayNode.removeChild(displayNode.firstChild);
            }

            let heading = document.createElement('h2');
            heading.style.textAlign = 'center'
            heading.style.paddingBottom = '50px'
            heading.innerText = `Top 20 users in ${country.toUpperCase()}, who work in ${language.toUpperCase()}`
            displayNode.appendChild(heading)

            cards = []

            for (let singleUser in clientRequest.response['items']){
                let login = clientRequest.response['items'][singleUser]['login'],
                    id = clientRequest.response['items'][singleUser]['id'],
                    avatar_url = clientRequest.response['items'][singleUser]['avatar_url'],
                    github_url = clientRequest.response['items'][singleUser]['html_url']
                let userCard = document.createElement('div');
                userCard.innerHTML = createCard(login, id, avatar_url, github_url);
                // displayNode.appendChild(userCard)
                cards.push(userCard)
            }

            for(let i = 0; i < cards.length - cards.length % 3; i = i + 3) {
                let cardDeck = document.createElement('div');
                cardDeck.className = 'card-deck'
                cardDeck.innerHTML = cards[i].innerHTML + cards[i+1].innerHTML + cards[i+2].innerHTML
                displayNode.appendChild(cardDeck)
            }
            
            if (cards.length % 3 == 1) {
                let cardDeck = document.createElement('div');
                cardDeck.className = 'card-deck'
                cardDeck.innerHTML = cards[cards.length - cards.length % 3].innerHTML
                displayNode.appendChild(cardDeck)
            } else if (cards.length % 3 == 2) {
                let cardDeck = document.createElement('div');
                cardDeck.className = 'card-deck'
                cardDeck.innerHTML = cards[cards.length - cards.length % 3].innerHTML + cards[cards.length - cards.length % 3 + 1].innerHTML
                displayNode.appendChild(cardDeck)
            } 
        }
    }

    clientRequest.send()
}

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
