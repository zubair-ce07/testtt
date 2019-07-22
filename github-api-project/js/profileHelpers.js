        // HELPER FUNCTION USED IN `profile.js` //

/**
 * Makes a new Github API request based on the given query
 *
 * @author: mabdullahz
 * @param {string} query API query to send
 * @returns {Promise} A promise that returns the requested data on resolve
 */
function githubAPICaller(query) {
    return new Promise(function(resolve, reject){
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
 * @param {string} option Specifies which query to generate
 * @returns {string} formatted query for API
 */
function generateQuery(option) {
    switch(option){
        case PROFILE_QUERY_OPTION:
            return `${API_BASE_URL}users/${USERNAME}`;
        case FOLLOWERS_QUERY_OPTION:
            return `${API_BASE_URL}users/${USERNAME}/followers?per_page=${NUMBER_OF_USERS_DISPLAYED}`;
        case FOLLOWING_QUERY_OPTION:
            return `${API_BASE_URL}users/${USERNAME}/following?per_page=${NUMBER_OF_USERS_DISPLAYED}`;
        case REPOS_QUERY_OPTION:
            return `${API_BASE_URL}users/${USERNAME}/repos?per_page=${NUMBER_OF_USERS_DISPLAYED}`;
    }
}


/**
 * Decides number of cards to be accomodated in each row
 *
 * @author: mabdullahz
 * @param {number} rowNumber Row number of cards
 * @param {number} repoCardsListLength Length of the repo card list
 * @returns {number} Number of cards in the specified row
 */
function countRemainingCards(rowNumber, repoCardsListLength) {
    return rowNumber + REPO_CARDS_PER_ROW <= repoCardsListLength
           ? REPO_CARDS_PER_ROW 
           : repoCardsListLength % REPO_CARDS_PER_ROW;
}


/**
 * Sets the button href in the various tabs
 *
 * @author: mabdullahz
 * @param {string} buttonID HTML ID of the button to select
 * @param {string} githubPage GitHub page to go to [followers, following]
 */
function fixButtonHref(buttonID, githubPage) {
    document.getElementById(buttonID).href = `https://github.com/${USERNAME}/${githubPage}`;
    document.getElementById(buttonID).target = "__blank";
}


/**
 * Deletes all children node from the specified tab
 *
 * @author: mabdullahz
 * @param {string} tabID HTML ID of the tab to select
 */
function emptyTab(tabID) {
    if(tabID != "home") {
        var tabElement = document.getElementById("display-" + tabID);

        while (tabElement.firstChild) {
            tabElement.removeChild(tabElement.firstChild);
        }
    }
}


/**
 * Modifies the given HTML `element` with new `value` for the `attribute`
 *
 * @author: mabdullahz
 * @param {string} elementID HTML ID of the element to select
 * @param {string} elementAttribute Attribute to modify
 * @param {string} newValue New value of the attribute
 */
function modifyHTMLElement(elementID, elementAttribute, newValue) {
    document.getElementById(elementID)[elementAttribute] = newValue;
}


/**
 * Format the given string URL by placing in an anchor tag
 *
 * @author: mabdullahz
 * @param {string} userBlog URl as a string
 * @returns {string} Specifying a formatted anchor tag
 */
function formatUserBlogInfo(userBlog){
    return `<a target="__blank" href=${userBlog}> ${userBlog} </a>`;
}


/**
 * Create a span element to show in place to empty data
 *
 * @author: mabdullahz
 * @param {string} nullReplacer Text value to use inside the span
 * @param {string} className Bootstrap class name to use inside the span
 * @returns {string} Specifying a formatted span tag
 */
function spanNullValue(nullReplacer, className) {
    return `<span class="bg-${className} text-center"> ${nullReplacer} </span>`;
}
