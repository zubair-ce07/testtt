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
 * Adds event listener to the tabbed profile div, listening for clicks
 *
 * @author: mabdullahz
 */
TABBED_PROFILE_ELEMENT.addEventListener("click", (event) => {
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
 * Displays the given user's followers from the API
 *
 * @author: mabdullahz
 * @param {object} returnedJsonData JSON data sent from the API
 */
function onloadUserFollowers(returnedJsonData) {
    displayUsers(FOLLOWERS_CARDS_DIV, returnedJsonData);

    fixButtonHref("display-followers-button", "followers");
}


/**
 * Displays the given user's following from the API
 *
 * @author: mabdullahz
 * @param {object} returnedJsonData JSON data sent from the API
 */
function onloadUserFollowing(returnedJsonData) {
    displayUsers(FOLLOWING_CARDS_DIV, returnedJsonData);

    fixButtonHref("display-following-button", "following");
}


/**
 * Displays the given user's repos from the API
 *
 * @author: mabdullahz
 * @param {object} returnedJsonData JSON data sent from the API
 */
function onloadUserRepos(returnedJsonData) {
    let repoCardsList = [];

    returnedJsonData.forEach((repo) => {
        repoCardsList.push(new Repository(repo[REPO_RESP_KEYS.fullName],
                           repo[REPO_RESP_KEYS.description] ? repo[REPO_RESP_KEYS.description] : spanNullValue("No Description Available", "warning"),
                           new Date(repo[REPO_RESP_KEYS.created]).toDateString(),
                           new Date(repo[REPO_RESP_KEYS.updated]).toDateString(),
                           repo[REPO_RESP_KEYS.watchers],
                           repo[REPO_RESP_KEYS.language] ? repo[REPO_RESP_KEYS.language] : spanNullValue("Unknown", "danger"),
                           repo[REPO_RESP_KEYS.forks],
                           repo[REPO_RESP_KEYS.issues],
                           repo[REPO_RESP_KEYS.license] ? repo[REPO_RESP_KEYS.license]["name"] : spanNullValue("Unknown", "danger"),
                           repo[REPO_RESP_KEYS.directURL]))
    })

    for(let i = 0; i < repoCardsList.length; i = i + REPO_CARDS_PER_ROW) {
        let cardDeck = document.createElement("div");
        cardDeck.className = CARD_CLASS_NAME;

        let remainingCards = countRemainingCards(i, repoCardsList.length)

        for(let j = i; j < i + remainingCards; j++) {
            cardDeck.appendChild(repoCardsList[j].generateRepoCard());
        }
        REPOS_CARDS_DIV.appendChild(cardDeck);
    }

    fixButtonHref("display-repositories-button", EMPTY_STRING);
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
        userCards.push(new User(index + 1,
                                singleUser[USER_RESP_KEYS.username],
                                singleUser[USER_RESP_KEYS.githubID],
                                singleUser[USER_RESP_KEYS.avatarURL],
                                singleUser[USER_RESP_KEYS.githubURL]));
    })

    for(let i = 0; i < userCards.length; i = i + USER_CARDS_PER_ROW) {
        let cardDeck = document.createElement("div");
        let remainingCards = i + USER_CARDS_PER_ROW <= userCards.length ? USER_CARDS_PER_ROW : userCards.length % USER_CARDS_PER_ROW;
        cardDeck.className = CARD_CLASS_NAME;

        for(let j = i; j < i + remainingCards; j++) {
            cardDeck.appendChild(userCards[j].generateUserCard());
        }

        mainDisplayElement.appendChild(cardDeck);
    }
}
