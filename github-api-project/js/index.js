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

/**
 * Makes a new Github API request based on the given query
 *
 * @author: mabdullahz
 * @param {string} query API query to send
 * @returns {Promise} A promise that returns the requested data on resolve
 */
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

/**
 * Generates the query and show the results when promise is resolved/rejected
 *
 * @author: mabdullahz
 * @param {string} country The country to search users in
 * @param {string} language The language used by the users
 * @param {string} criteria The criteria used to sort the users
 */
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

/**
 * Makes the spinner loader visible
 *
 * @author: mabdullahz
 */
function showSpinner() {
    SPINNER_LOADER.style.visibility = "visible";
}

/**
 * Hides the spinner loader
 *
 * @author: mabdullahz
 */
function hideSpinner() {
    SPINNER_LOADER.style.visibility = "hidden";
}

/**
 * Checks the country field
 *
 * @author: mabdullahz
 * @returns {boolean} Specifying whether the field is empty or filled
 */
function emptyCountryArg() {
    return (COUNTRY_ELEMENT.value == EMPTY_STRING);
}

/**
 * Checks the criteria field
 *
 * @author: mabdullahz
 * @returns {boolean} Specifying whether a criteria has been selected or not
 */
function emptyCriteriaArg() {
    return (CRITERIA_ELEMENT.value == EMPTY_STRING);
}

/**
 * Checks the language field
 *
 * @author: mabdullahz
 * @returns {boolean} Specifying whether a language has been selected or not
 */
function emptyLanguageArg() {
    return (LANGUAGE_ELEMENT.value == EMPTY_STRING);
}

/**
 * Appends warning text in country field
 *
 * @author: mabdullahz
 */
function showCountryWarning() {
    COUNTRY_WARNING_DIV.innerText = COUNTRY_WARNING;
}

/**
 * Appends warning text in language field
 *
 * @author: mabdullahz
 */
function showLanguageWarning() {
    LANGUAGE_WARNING_DIV.innerText = LANGUAGE_WARNING;
}

/**
 * Appends warning text in criteria field
 *
 * @author: mabdullahz
 */
function showCriteriaWarning() {
    CRITERIA_WARNING_DIV.innerText = CRITERIA_WARNING;
}

/**
 * Deletes warning text from country field
 *
 * @author: mabdullahz
 */
function hideCountryWarning() {
    COUNTRY_WARNING_DIV.innerText = EMPTY_STRING;
}


/**
 * Deletes warning text from language field
 *
 * @author: mabdullahz
 */
function hideLanguageWarning() {
    LANGUAGE_WARNING_DIV.innerText = EMPTY_STRING;
}

/**
 * Deletes warning text from criteria field
 *
 * @author: mabdullahz
 */
function hideCriteriaWarning() {
    CRITERIA_WARNING_DIV.innerText = EMPTY_STRING;
}

/**
 * Checks whether all required fields are filled and shows warnings
 *
 * @author: mabdullahz
 * @returns {boolean} Specifying whether all fields are filled or not
 */
function validateGithubAPIArgs() {
    emptyCountryArg() ? showCountryWarning() : hideCountryWarning();
    emptyLanguageArg() ? showLanguageWarning() : hideLanguageWarning();
    emptyCriteriaArg() ? showCriteriaWarning() : hideCriteriaWarning();
    
    return (!emptyCountryArg() && !emptyCriteriaArg() && !emptyLanguageArg());
}

/**
 * Displays the users given the data from the API
 *
 * @author: mabdullahz
 * @param {object} returnedJsonData JSON data sent from the API
 */
function userInfoOnLoad(returnedJsonData) {
    const API_RESPONSE = returnedJsonData;
    let userCards = [];
    var mainDisplayElement = document.getElementById("disp");

    removeAllChildren("disp");
    removeCustomStyle("disp");
    
    let heading = createHTMLElement("h2", 
                                    {"textAlign": "center", "paddingBottom": "50px"}, 
                                    `By ${CRITERIA_ELEMENT.value.toUpperCase()}: Top 
                                        ${NUMBER_OF_USERS_DISPLAYED}/${API_RESPONSE["total_count"]} 
                                        users in <u>${COUNTRY_ELEMENT.value.toUpperCase()}</u>, who work in 
                                        <i>${LANGUAGE_ELEMENT.value.toUpperCase()}</i>`);

    mainDisplayElement.appendChild(heading);
    
    API_RESPONSE["items"].forEach((singleUser, index) => {
        userCards.push(new User(index + 1, singleUser[USER_API_RESP_STRUCT.username], singleUser[USER_API_RESP_STRUCT.githubID], singleUser[USER_API_RESP_STRUCT.avatarURL], singleUser[USER_API_RESP_STRUCT.githubURL]));
    })

    for(let i = 0; i < userCards.length; i = i + USER_CARDS_PER_ROW) {
        let cardDeck = document.createElement("div");
        cardDeck.className = "card-deck";

        let remainingCards = i + USER_CARDS_PER_ROW <= userCards.length ? USER_CARDS_PER_ROW : userCards.length % USER_CARDS_PER_ROW;

        for(let j = i; j < i + remainingCards; j++) {
            cardDeck.appendChild(userCards[j].generateUserCard());
        }
        mainDisplayElement.appendChild(cardDeck);
    }

    let endText = createHTMLElement("h4", 
                                    {"textAlign": "center", "marginTop": "50px"},
                                    `... End of Results ...`);
    mainDisplayElement.appendChild(endText);
}

/**
 * Creates a new HTML element
 *
 * @author: mabdullahz
 * @param {string} elementType Type of element to create e.g. h1, div 
 * @param {object} elementStyleInfo Key/value paired object specifying design
 * @param {string} elementInnerHTML Inner HTML of the element, if any
 * @returns {object} Newly created HTML element
 */
function createHTMLElement(elementType, elementStyleInfo, elementInnerHTML) {
    let newElement = document.createElement(elementType);

    for(eachAttribute in elementStyleInfo){
        let attributeValue = elementStyleInfo[eachAttribute];
        newElement.style[eachAttribute] = attributeValue;
    }

    newElement.innerHTML = elementInnerHTML;

    return newElement;
}

/**
 * Removes all styling applied to the specified element
 *
 * @author: mabdullahz
 * @param {string} elementID HTML ID of the element
 */
function removeCustomStyle(elementID) {
    var selectedElement = document.getElementById(elementID);
    selectedElement.style = EMPTY_STRING;
}

/**
 * Removes all children of the specified element
 *
 * @author: mabdullahz
 * @param {string} elementID HTML ID of the element
 */
function removeAllChildren(elementID) {
    var selectedElement = document.getElementById(elementID);
    while (selectedElement.firstChild) {
        selectedElement.removeChild(selectedElement.firstChild);
    }
}
