const COUNTRY_ELEMENT = document.getElementById("countrySelector");
const LANGUAGE_ELEMENT = document.getElementById("languageSelector");
const CRITERIA_ELEMENT = document.getElementById("criteriaSelector");
const API_ARGS_FORM = document.getElementById("argumentHandler");
const CARDS_DISPLAY_DIV = document.getElementById("disp");

const LANGUAGE_WARNING = {div: document.getElementById("emptyLang"), text: "Please select a language!"}
const COUNTRY_WARNING = {div: document.getElementById("emptyCountry"), text: "You must type in a Country"}
const CRITERIA_WARNING = {div: document.getElementById("emptyCriteria"), text: "Please select a criteria!"}

const CARD_CLASS_NAMES = "card text-white bg-secondary mb-3 border-success";
const CARD_STYLE = "width: 18rem;";

validateGithubAPIArgs();

API_ARGS_FORM.addEventListener(EVENT_TO_LISTEN, (event) => {
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
    return new Promise(function(resolve, reject) {
        let clientRequest = new XMLHttpRequest();

        clientRequest.open(REQ_METHOD, query, ASYNC_API_CALL);
        clientRequest.responseType = RES_TYPE;
        clientRequest.onload = function() {
            if (clientRequest.status == API_REQUEST_SUCCESSFUL) {
                resolve(clientRequest.response);
            } else {
                reject(new Error(REQUEST_FAILED_MESSAGE));
            }
        }
        clientRequest.send();
    })
}


/**
 * Generates the search user query
 *
 * @author: mabdullahz
 * @param {string} country The country to search users in
 * @param {string} language The language used by the users
 * @param {string} criteria The criteria used to sort the users
 * @returns {string} formatted query for API
 */
function generateFetchUsersQuery(country, language, criteria) {
    return `${API_BASE_URL}search/users?o=desc&q=language%3A${encodeURIComponent(language)}+location%3A${country}&sort=${criteria}&type=users&per_page=${NUMBER_OF_USERS_DISPLAYED}`;
}


/**
 * Fetches the users to display
 *
 * @author: mabdullahz
 * @param {string} country The country to search users in
 * @param {string} language The language used by the users
 * @param {string} criteria The criteria used to sort the users
 */
function fetchUsers(country, language, criteria) {
    const QUERY = generateFetchUsersQuery(country, language, criteria);

    changeLoaderSpinnerState(VISIBILITY_OPTION_ON);
    githubAPICaller(QUERY)
    .then((returnedJsonData) => {
        userInfoOnLoad(returnedJsonData);
    })
    .catch((e) => {
        console.log(e);
    })
    .finally(() => {
        changeLoaderSpinnerState(VISIBILITY_OPTION_OFF);
    })
}


/**
 * Changes the spinner state based on the given argument
 *
 * @author: mabdullahz
 * @param {string} Specifies the state of spinner to change to
 */
function changeLoaderSpinnerState(option) {
    SPINNER_LOADER.style.visibility = option;
}


/**
 * Checks if the specified arg field is empty
 *
 * @author: mabdullahz
 * @param {object} HTML object to check whether it is empty
 * @returns {boolean} Specifying whether the field is empty or filled
 */
function isArgFormFieldEmpty(argFormField) {
    return (argFormField.value == EMPTY_STRING);
}


/**
 * Appends warning text in country field
 *
 * @author: mabdullahz
 * @param {object} Key-value paired object specifying warning div and text 
 */
function showWarningTextDiv(warningObject) {
    warningObject.div.innerText = warningObject.text;
}


/**
 * Deletes warning text from country field
 *
 * @author: mabdullahz
 * @param {object} Key-value paired object specifying warning div and text 
 */
function hideWarningTextDiv(warningObject) {
    warningObject.div.innerText = EMPTY_STRING;
}


/**
 * Checks whether all required fields are filled and shows warnings
 *
 * @author: mabdullahz
 * @returns {boolean} Specifying whether all fields are filled or not
 */
function validateGithubAPIArgs() {
    let countryFillStatus = isArgFormFieldEmpty(COUNTRY_ELEMENT);
    let languageFillStatus = isArgFormFieldEmpty(LANGUAGE_ELEMENT);
    let criteriaFillStatus = isArgFormFieldEmpty(CRITERIA_ELEMENT);

    countryFillStatus ? showWarningTextDiv(COUNTRY_WARNING) : hideWarningTextDiv(COUNTRY_WARNING);
    languageFillStatus ? showWarningTextDiv(LANGUAGE_WARNING) : hideWarningTextDiv(LANGUAGE_WARNING);
    criteriaFillStatus ? showWarningTextDiv(CRITERIA_WARNING) : hideWarningTextDiv(CRITERIA_WARNING);
    
    return (!countryFillStatus &&
            !languageFillStatus &&
            !criteriaFillStatus);
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
    
    removeAllChildren(CARDS_DISPLAY_DIV);
    removeCustomStyle(CARDS_DISPLAY_DIV);
    
    let heading = createHTMLElement("h2", 
                                    {"textAlign": "center", "paddingBottom": "50px"}, 
                                    `By ${CRITERIA_ELEMENT.value.toUpperCase()}: Top 
                                        ${NUMBER_OF_USERS_DISPLAYED}/${API_RESPONSE["total_count"]} 
                                        users in <u>${COUNTRY_ELEMENT.value.toUpperCase()}</u>, who work in 
                                        <i>${LANGUAGE_ELEMENT.value.toUpperCase()}</i>`);

    CARDS_DISPLAY_DIV.appendChild(heading);
    
    API_RESPONSE["items"].forEach((singleUser, index) => {
        userCards.push(new User(index + 1, 
                                singleUser[USER_API_RESP_STRUCT.username], 
                                singleUser[USER_API_RESP_STRUCT.githubID], 
                                singleUser[USER_API_RESP_STRUCT.avatarURL], 
                                singleUser[USER_API_RESP_STRUCT.githubURL]));
    })

    for(let i = 0; i < userCards.length; i = i + USER_CARDS_PER_ROW) {
        let cardDeck = document.createElement("div");
        cardDeck.className = CARD_CLASS_NAME;

        let remainingCards = i + USER_CARDS_PER_ROW <= userCards.length ? USER_CARDS_PER_ROW : userCards.length % USER_CARDS_PER_ROW;

        for(let j = i; j < i + remainingCards; j++) {
            cardDeck.appendChild(userCards[j].generateUserCard());
        }
        CARDS_DISPLAY_DIV.appendChild(cardDeck);
    }

    let endText = createHTMLElement("h4", 
                                    {"textAlign": "center", "marginTop": "50px"},
                                    `... End of Results ...`);
    CARDS_DISPLAY_DIV.appendChild(endText);
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
 * @param {object} HTML element
 */
function removeCustomStyle(html_element) {
    html_element.style = EMPTY_STRING;
}

/**
 * Removes all children of the specified element
 *
 * @author: mabdullahz
 * @param {object} HTML element
 */
function removeAllChildren(html_element) {
    while (html_element.firstChild) {
        html_element.removeChild(html_element.firstChild);
    }
}
