import {addNews} from "./actions/index";

//_______________________Application constants____________________________

const domain = "http://127.0.0.1:8000/api";

// ______________________Configure functions__________________________

function getRequestHeader() {
    if (localStorage.authToken) {
        return {
            Authorization: 'Token ' + localStorage.authToken,
            'Content-Type': 'application/json',
        };
    }
    return {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
}


const updateStoreState = (store, newsJson) => {
    if (Array.isArray(newsJson)) {
        newsJson.forEach((news) => {
            store.dispatch(addNews(news));
        });
    } else {
        store.dispatch(addNews(newsJson));
    }
};

const loadNewsFromAPI = (store, id) => {
    let link = domain + '/news/';
    link += id ? id : '';
    return fetch(link, {
        method: 'GET',
        headers: getRequestHeader()
    })
        .then((response) => response.json())
        .then((newsJson) => {
            updateStoreState(store, newsJson)
        })
        .catch((error) => {
            console.error(error);
        });
};

export {domain, getRequestHeader, loadNewsFromAPI};
