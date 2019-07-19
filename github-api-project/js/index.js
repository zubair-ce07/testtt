const COUNTRY_ELEMENT = document.getElementById("countrySelector");
const LANGUAGE_ELEMENT = document.getElementById("languageSelector");
const CRITERIA_ELEMENT = document.getElementById("criteriaSelector");
const COUNTRY_WARNING_DIV = document.getElementById("emptyCountry");
const LANGUAGE_WARNING_DIV = document.getElementById("emptyLang");
const CRITERIA_WARNING_DIV = document.getElementById("emptyCriteria");
const SPINNER_LOADER = document.getElementById("spinnerLoader");
const COUNTRY_WARNING = "You must type in a Country";
const LANGUAGE_WARNING = "Please select a language!";
const CRITERIA_WARNING = "Please select a criteria!";
const NUMBER_OF_USERS_DISPLAYED = 20;
const API_BASE_URL = "https://api.github.com/";
const ASYNC_API_CALL = true;
const API_REQUEST_SUCCESSFUL = 200;
const REQ_METHOD = "GET";
const RES_TYPE = "json";
const USER_CARDS_PER_ROW = 4;
const EMPTY_STRING = "";
const CARD_CLASS_NAMES = "card text-white bg-secondary mb-3 border-success";
const CARD_STYLE = "width: 18rem;";

const USER_API_RESP_STRUCT = {
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
};


document.getElementById("argumentHandler").addEventListener("change", (event) => {
    if(validateGithubAPIArgs()) {
        fetchUsers(COUNTRY_ELEMENT.value, LANGUAGE_ELEMENT.value, CRITERIA_ELEMENT.value);
    }
})


function githubAPICaller(query) {
    return new Promise(function(resolve, reject) {;
        let clientRequest = new XMLHttpRequest()

        clientRequest.open(REQ_METHOD, query, ASYNC_API_CALL);
        clientRequest.responseType = RES_TYPE;
        clientRequest.onload = function() {
            if (clientRequest.status == API_REQUEST_SUCCESSFUL) {
                resolve(clientRequest.response);
            } else {
                reject(new Error('Failed 200 OK => API Request was not Successful!'));
            }
        }
        clientRequest.send();
    })
}


function fetchUsers(country, language, criteria) {
    const QUERY = `${API_BASE_URL}search/users?o=desc&q=language%3A${encodeURIComponent(language)}+location%3A${country}&sort=${criteria}&type=users&per_page=${NUMBER_OF_USERS_DISPLAYED}`;

    showSpinner();
    githubAPICaller(QUERY)
    .then((returnedJsonData) => {
        userInfoOnLoad(returnedJsonData);
    })
    .catch((e) => {
        console.log(e);
    })
    .finally(() => {
        hideSpinner();
    })
}


function showSpinner() {
    SPINNER_LOADER.style.visibility = "visible";
}


function hideSpinner() {
    SPINNER_LOADER.style.visibility = "hidden";
}


function emptyCountryArg() {
    return (COUNTRY_ELEMENT.value == EMPTY_STRING);
}


function emptyCriteriaArg() {
    return (CRITERIA_ELEMENT.value == EMPTY_STRING);
}


function emptyLanguageArg() {
    return (LANGUAGE_ELEMENT.value == EMPTY_STRING);
}


function showCountryWarning() {
    COUNTRY_WARNING_DIV.innerText = COUNTRY_WARNING;
}


function showLanguageWarning() {
    LANGUAGE_WARNING_DIV.innerText = LANGUAGE_WARNING;
}


function showCriteriaWarning() {
    CRITERIA_WARNING_DIV.innerText = CRITERIA_WARNING;
}


function hideCountryWarning() {
    COUNTRY_WARNING_DIV.innerText = EMPTY_STRING;
}


function hideLanguageWarning() {
    LANGUAGE_WARNING_DIV.innerText = EMPTY_STRING;
}


function hideCriteriaWarning() {
    CRITERIA_WARNING_DIV.innerText = EMPTY_STRING;
}


function validateGithubAPIArgs() {
    emptyCountryArg() ? showCountryWarning() : hideCountryWarning();
    emptyLanguageArg() ? showLanguageWarning() : hideLanguageWarning();
    emptyCriteriaArg() ? showCriteriaWarning() : hideCriteriaWarning();
    
    return (!emptyCountryArg() && !emptyCriteriaArg() && !emptyLanguageArg());
}


function userInfoOnLoad(returnedJsonData) {
    const API_RESPONSE = returnedJsonData;
    let userCards = [];
    var mainDisplayElement = document.getElementById("disp");

    removeAllChildren("disp");
    removeCustomStyle(mainDisplayElement);
    
    let heading = createHTMLElement("h2", 
                                    {"textAlign": "center", "paddingBottom": "50px"}, 
                                    `By ${CRITERIA_ELEMENT.value.toUpperCase()}: Top 
                                        ${NUMBER_OF_USERS_DISPLAYED}/${API_RESPONSE["total_count"]} 
                                        users in <u>${COUNTRY_ELEMENT.value.toUpperCase()}</u>, who work in 
                                        <i>${LANGUAGE_ELEMENT.value.toUpperCase()}</i>`);

    mainDisplayElement.appendChild(heading);
    
    API_RESPONSE["items"].forEach((singleUser, index) => {
        userCards.push(createOneUserCard(index + 1, singleUser[USER_API_RESP_STRUCT.username], singleUser[USER_API_RESP_STRUCT.githubID], singleUser[USER_API_RESP_STRUCT.avatarURL], singleUser[USER_API_RESP_STRUCT.githubURL]));
    })

    for(let i = 0; i < userCards.length; i = i + USER_CARDS_PER_ROW) {
        let cardDeck = document.createElement("div");
        cardDeck.className = "card-deck";

        let remainingCards = i + USER_CARDS_PER_ROW <= userCards.length ? USER_CARDS_PER_ROW : userCards.length % USER_CARDS_PER_ROW;

        for(let j = i; j < i + remainingCards; j++) {
            cardDeck.appendChild(userCards[j]);
        }
        mainDisplayElement.appendChild(cardDeck);
    }

    let endText = createHTMLElement("h4", 
                                    {"textAlign": "center", "marginTop": "50px"},
                                    `... End of Results ...`);
    mainDisplayElement.appendChild(endText);
}


function createHTMLElement(elementType, elementStyleInfo, elementInnerHTML) {
    let newElement = document.createElement(elementType);

    for(eachAttribute in elementStyleInfo){
        let attributeValue = elementStyleInfo[eachAttribute];
        newElement.style[eachAttribute] = attributeValue;
    }

    newElement.innerHTML = elementInnerHTML;

    return newElement;
}


function removeCustomStyle(mainDisplayElement) {
    mainDisplayElement.style = EMPTY_STRING;
}


function createOneUserCard(number, username, id, avatar_url, github_url) {
    let userCard = document.createElement('div');
    userCard.className = CARD_CLASS_NAMES;
    userCard.style = CARD_STYLE;
    userCard.innerHTML = `<div class="card-header text-bold">${number}</div>
                            <img class="card-img-top" src="${avatar_url}" alt="Card image cap">

                            <div class="card-body">
                                <h5 class="card-title text-center">${username}</h5>
                            </div>

                            <div class="card-footer bg-secondary text-center">
                                <a href="profile.html?username=${username}" class="btn btn-success">View Profile</a>
                            </div>
                        </div>`;
    return userCard;
}


function removeAllChildren(elementID) {
    var mainDisplayElement = document.getElementById(elementID);
    while (mainDisplayElement.firstChild) {
        mainDisplayElement.removeChild(mainDisplayElement.firstChild);
    }
}
