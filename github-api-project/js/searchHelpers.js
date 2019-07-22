        // HELPER FUNCTION USED IN `search.js` //

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
