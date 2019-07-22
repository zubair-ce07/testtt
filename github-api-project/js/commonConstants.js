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
