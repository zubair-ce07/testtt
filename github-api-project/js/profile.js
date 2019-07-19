const USERNAME = new URL(window.location).searchParams.get("username");
const TABBED_PROFILE_ELEMENT = document.getElementById("user-profile-page");
const HOME_TAB = "#home";
const FOLLOWERS_TAB = "#followers";
const FOLLOWING_TAB = "#following";
const REPOS_TAB = "#repositories";
const FOLLOWERS_CARDS_DIV = document.getElementById("display-followers");
const FOLLOWING_CARDS_DIV = document.getElementById("display-following");
const REPOS_CARDS_DIV = document.getElementById("display-repositories");

const PROFILE_QUERY_OPTION = "profile";
const FOLLOWERS_QUERY_OPTION = "followers";
const FOLLOWING_QUERY_OPTION = "following";
const REPOS_QUERY_OPTION = "repos";

const REPO_CARDS_PER_ROW = 2;
const JSON_NULL = "-";
const CARD_CLASS_NAMES = "card text-white bg-secondary mb-3 border-success";
const CARD_STYLE = "width: 18rem;";

let previousTab = null;

if(USERNAME != null){
    document.getElementById("username").innerText = USERNAME;
    fetchUser();
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
 * Adds event listener to the tabbed profile div, listening for clicks
 *
 * @author: mabdullahz
 */
TABBED_PROFILE_ELEMENT.addEventListener(EVENT_TO_LISTEN, (event) => {
    const targetTab = event.target.getAttribute("href");

    if(previousTab != targetTab && targetTab != null) {
        let tabIdWithoutHashTag = targetTab.split("#")[1];
        emptyTab(tabIdWithoutHashTag);
        previousTab = targetTab;

        if(targetTab == HOME_TAB) {
            fetchUser();
        } else if(targetTab == FOLLOWERS_TAB) {
            fetchFollowers();
        } else if(targetTab == FOLLOWING_TAB) {
            fetchFollowing();
        } else if(targetTab == REPOS_TAB) {
            fetchRepos();
        }
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
 * Generates the query and show the user info when promise is resolved/rejected
 *
 * @author: mabdullahz
 */
function fetchUser(){
    const QUERY = generateQuery(PROFILE_QUERY_OPTION);

    changeLoaderSpinnerState(VISIBILITY_OPTION_ON);
    githubAPICaller(QUERY)
    .then((returnedJsonData)=> {
        onloadUserInfo(returnedJsonData);
    })
    .catch((e) => {
        console.log(e);
    })
    .finally(() => {
        changeLoaderSpinnerState(VISIBILITY_OPTION_OFF);
    })
}

/**
 * Generates the query and show the followers when promise is resolved/rejected
 *
 * @author: mabdullahz
 */
function fetchFollowers() {
    let QUERY = generateQuery(FOLLOWERS_QUERY_OPTION);

    changeLoaderSpinnerState(VISIBILITY_OPTION_ON);
    githubAPICaller(QUERY)
    .then((returnedJsonData)=> {
        onloadUserFollowers(returnedJsonData);
    })
    .catch((e) => {
        console.log(e);
    })
    .finally(() => {
        changeLoaderSpinnerState(VISIBILITY_OPTION_OFF);
    })
}

/**
 * Generates the query and show the following when promise is resolved/rejected
 *
 * @author: mabdullahz
 */
function fetchFollowing() {
    let QUERY = generateQuery(FOLLOWING_QUERY_OPTION);

    changeLoaderSpinnerState(VISIBILITY_OPTION_ON);
    githubAPICaller(QUERY)
    .then((returnedJsonData)=> {
        onloadUserFollowing(returnedJsonData);
    })
    .catch((e) => {
        console.log(e);
    })
    .finally(() => {
        changeLoaderSpinnerState(VISIBILITY_OPTION_OFF);
    })
}

/**
 * Generates the query and show the repos when promise is resolved/rejected
 *
 * @author: mabdullahz
 */
function fetchRepos() {
    let QUERY = generateQuery(REPOS_QUERY_OPTION);

    changeLoaderSpinnerState(VISIBILITY_OPTION_ON);
    githubAPICaller(QUERY)
    .then((returnedJsonData)=> {
        onloadUserRepos(returnedJsonData);
    })
    .catch((e) => {
        console.log(e);
    })
    .finally(() => {
        changeLoaderSpinnerState(VISIBILITY_OPTION_OFF);
    })
}

/**
 * Displays the given user's data from the API
 *
 * @author: mabdullahz
 * @param {object} userInfo JSON data sent from the API
 */
function onloadUserInfo(userInfo) {
    let userJoinedDate = new Date(userInfo[USER_API_RESP_STRUCT.joinedAt]);

    modifyHTMLElement("avatar", "src", userInfo[USER_API_RESP_STRUCT.avatarURL]);
    modifyHTMLElement("github-url", "href", userInfo[USER_API_RESP_STRUCT.githubURL]);
    modifyHTMLElement("github-url", "target", "__blank");
    modifyHTMLElement("real-name", "innerText", userInfo[USER_API_RESP_STRUCT.fullName]);
    modifyHTMLElement("user-location", "innerText", userInfo[USER_API_RESP_STRUCT.location] ? userInfo[USER_API_RESP_STRUCT.location] : JSON_NULL);
    modifyHTMLElement("user-company", "innerText", userInfo[USER_API_RESP_STRUCT.company] ? userInfo[USER_API_RESP_STRUCT.company] : JSON_NULL);
    modifyHTMLElement("user-bio", "innerText", userInfo[USER_API_RESP_STRUCT.bio] ? userInfo[USER_API_RESP_STRUCT.bio] : EMPTY_STRING);
    modifyHTMLElement("user-joined", "innerText", `${userJoinedDate.getDay()}/${userJoinedDate.getMonth()}/${userJoinedDate.getFullYear()}`);
    modifyHTMLElement("user-blog", "innerHTML", userInfo[USER_API_RESP_STRUCT.blogURL] ? formatUserBlogInfo(userInfo[USER_API_RESP_STRUCT.blogURL]) : JSON_NULL);
    modifyHTMLElement("user-followers-badge", "innerText", userInfo[USER_API_RESP_STRUCT.followersURL]);
    modifyHTMLElement("user-following-badge", "innerText", userInfo[USER_API_RESP_STRUCT.followingURL]);
    modifyHTMLElement("user-repos-badge", "innerText", userInfo[USER_API_RESP_STRUCT.reposURL]);
}

/**
 * Displays the given user's followers from the API
 *
 * @author: mabdullahz
 * @param {object} returnedJsonData JSON data sent from the API
 */
function onloadUserFollowers(returnedJsonData) {
    let mainDisplayElement = document.getElementById(FOLLOWERS_CARDS_DIV);
    displayUsers(mainDisplayElement, returnedJsonData);

    fixButtonHref("display-followers-button", "followers");
}

/**
 * Displays the given user's following from the API
 *
 * @author: mabdullahz
 * @param {object} returnedJsonData JSON data sent from the API
 */
function onloadUserFollowing(returnedJsonData) {
    let mainDisplayElement = document.getElementById(FOLLOWING_CARDS_DIV);
    displayUsers(mainDisplayElement, returnedJsonData);

    fixButtonHref("display-following-button", "following");
}

/**
 * Displays the given user's repos from the API
 *
 * @author: mabdullahz
 * @param {object} returnedJsonData JSON data sent from the API
 */
function onloadUserRepos(returnedJsonData) {
    let mainDisplayElement = document.getElementById(REPOS_CARDS_DIV);
    let repoCardsList = [];

    returnedJsonData.forEach((repo) => {
        repoCardsList.push(new Repo(repo[REPO_API_RESP_STRUCT.fullName],
                           repo[REPO_API_RESP_STRUCT.description] ? repo[REPO_API_RESP_STRUCT.description] : spanNullValue("No Description Available", "warning"),
                           new Date(repo[REPO_API_RESP_STRUCT.created]).toDateString(),
                           new Date(repo[REPO_API_RESP_STRUCT.updated]).toDateString(),
                           repo[REPO_API_RESP_STRUCT.watchers],
                           repo[REPO_API_RESP_STRUCT.language] ? repo[REPO_API_RESP_STRUCT.language] : spanNullValue("Unknown", "danger"),
                           repo[REPO_API_RESP_STRUCT.forks],
                           repo[REPO_API_RESP_STRUCT.issues],
                           repo[REPO_API_RESP_STRUCT.license] ? repo[REPO_API_RESP_STRUCT.license]["name"] : spanNullValue("Unknown", "danger"),
                           repo[REPO_API_RESP_STRUCT.directURL]))
    })

    for(let i = 0; i < repoCardsList.length; i = i + REPO_CARDS_PER_ROW) {
        let cardDeck = document.createElement("div");
        cardDeck.className = "card-deck";
        let remainingCards = i + REPO_CARDS_PER_ROW <= repoCardsList.length ? REPO_CARDS_PER_ROW : repoCardsList.length % REPO_CARDS_PER_ROW;
        for(let j = i; j < i + remainingCards; j++) {
            cardDeck.appendChild(repoCardsList[j].generateRepoCard());
        }
        mainDisplayElement.appendChild(cardDeck);
    }

    fixButtonHref("display-repositories-button", EMPTY_STRING);
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

/**
 * Displays the users given the API response data in form of rowed cards
 *
 * @author: mabdullahz
 * @param {object} mainDisplayElement HTML element to display the results inside of
 * @param {object} apiCallResult JSON data sent from the API
 */
function displayUsers(mainDisplayElement, apiCallResult) {
    let userCards = [];

    apiCallResult.forEach((singleUser, index) => {
        userCards.push(new User(index + 1, singleUser[USER_API_RESP_STRUCT.username], singleUser[USER_API_RESP_STRUCT.githubID], singleUser[USER_API_RESP_STRUCT.avatarURL], singleUser[USER_API_RESP_STRUCT.githubURL]));
    })

    for(let i = 0; i < userCards.length; i = i + USER_CARDS_PER_ROW) {
        let cardDeck = document.createElement("div");
        let remainingCards = i + USER_CARDS_PER_ROW <= userCards.length ? USER_CARDS_PER_ROW : userCards.length % USER_CARDS_PER_ROW;
        cardDeck.className = "card-deck";

        for(let j = i; j < i + remainingCards; j++) {
            cardDeck.appendChild(userCards[j].generateUserCard());
        }

        mainDisplayElement.appendChild(cardDeck);
    }
}
