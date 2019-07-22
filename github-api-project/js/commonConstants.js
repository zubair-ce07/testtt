const API_BASE_URL = "https://api.github.com/";
const REQ_METHOD = "GET";
const RES_TYPE = "json";
const API_REQUEST_SUCCESSFUL = 200;
const ASYNC_API_CALL = true;
const USER_CARDS_PER_ROW = 4;
const EMPTY_STRING = "";
const SPINNER_LOADER = document.getElementById("spinnerLoader");
const NUMBER_OF_USERS_DISPLAYED = 20;
const REQUEST_FAILED_MESSAGE = "Failed 200 OK => API Request was not successful!";
const VISIBILITY_OPTION_ON = "visible";
const VISIBILITY_OPTION_OFF = "hidden";
const EVENT_TO_LISTEN = "change";
const CARD_CLASS_NAME = "card-deck";

const USER_RESP_KEYS = {
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

const REPO_RESP_KEYS = {
        fullName: "name",
        description: "description",
        created: "created_at",
        updated: "updated_at",
        watchers: "watchers_count",
        language: "language",
        forks: "forks_count",
        issues: "open_issues_count",
        license: "license",
        directURL: "html_url",
};


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
