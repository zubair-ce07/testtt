import axios from 'axios';

import {SEARCH_MOVIE, SEARCHING, ROOT_URL, SEARCH_USER} from './action_types'


export function searchMovie(term) {
    const request = axios.get(`${ROOT_URL}/api/search/?q=${term}`);
    return {
        type: SEARCH_MOVIE,
        payload: request
    };
}

export function requestingSearch() {
    return {
        type: SEARCHING,
        payload: 'fetching'
    };
}

export function searchUser(term) {
    const request = axios.get(`${ROOT_URL}/api/users/search/?q=${term}`);
    return {
        type: SEARCH_USER,
        payload: request
    };
}
