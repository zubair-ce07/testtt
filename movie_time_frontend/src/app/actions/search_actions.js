import axios from 'axios';

import {SEARCH_MOVIE, SEARCHING_MOVIE, ROOT_URL} from './action_types'


export function searchMovie(term) {
    const request = axios.get(`${ROOT_URL}/api/search/?q=${term}`);
    return {
        type: SEARCH_MOVIE,
        payload: request
    };
}

export function requestingSearchMovie() {
    return {
        type: SEARCHING_MOVIE,
        payload: 'fetching'
    };
}
