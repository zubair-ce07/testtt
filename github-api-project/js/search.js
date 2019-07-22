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

API_ARGS_FORM.addEventListener('keypress', (e) => {
    if(e.keyCode == 13) {
        e.preventDefault()
        if(validateGithubAPIArgs()) {
            fetchUsers(COUNTRY_ELEMENT.value, LANGUAGE_ELEMENT.value, CRITERIA_ELEMENT.value);
        }
    }
})


API_ARGS_FORM.addEventListener(EVENT_TO_LISTEN, (event) => {
    if(validateGithubAPIArgs()) {
        fetchUsers(COUNTRY_ELEMENT.value, LANGUAGE_ELEMENT.value, CRITERIA_ELEMENT.value);
    }
})


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
 * Displays the users given the data from the API
 *
 * @author: mabdullahz
 * @param {object} returnedJsonData JSON data sent from the API
 */
function userInfoOnLoad(API_RESPONSE) {
    
    removeAllChildren(CARDS_DISPLAY_DIV);
    removeCustomStyle(CARDS_DISPLAY_DIV);
    
    let heading = createHTMLElement("h2", 
                                    {"textAlign": "center", "paddingBottom": "50px"}, 
                                    `By ${CRITERIA_ELEMENT.value.toUpperCase()}: Top 
                                        ${NUMBER_OF_USERS_DISPLAYED}/${API_RESPONSE["total_count"]} 
                                        users in <u>${COUNTRY_ELEMENT.value.toUpperCase()}</u>, who work in 
                                        <i>${LANGUAGE_ELEMENT.value.toUpperCase()}</i>`);

    CARDS_DISPLAY_DIV.appendChild(heading);


    displayUsers(CARDS_DISPLAY_DIV, API_RESPONSE["items"])


    let endText = createHTMLElement("h4", 
                                    {"textAlign": "center", "marginTop": "50px"},
                                    `... End of Results ...`);

    CARDS_DISPLAY_DIV.appendChild(endText);
}
