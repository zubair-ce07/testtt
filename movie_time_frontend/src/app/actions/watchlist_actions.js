import axios from 'axios';

import {
    ADD_TO_WATCHLIST,
    REMOVE_FROM_WATCHLIST,
    GET_TO_WATCH_LIST,
    VOTE_ACTOR,
    GET_WATCHED_LIST,
    GET_UPCOMING_LIST,
    UPDATE_WATCHLIST,
    RATE_MOVIE,
    ROOT_URL
} from './action_types';


export function fetchToWatchList() {
    const request = axios.get(`${ROOT_URL}/api/to-watch/`);

    return {
        type: GET_TO_WATCH_LIST,
        payload: request
    };
}

export function fetchWatchedList() {
    const request = axios.get(`${ROOT_URL}/api/watched/`);

    return {
        type: GET_WATCHED_LIST,
        payload: request
    };
}

export function fetchUpcomingList() {
    const request = axios.get(`${ROOT_URL}/api/upcoming/`);

    return {
        type: GET_UPCOMING_LIST,
        payload: request
    };
}

export function addToWatchlist(movie_id) {
    const request = axios.put(`${ROOT_URL}/api/movies/${movie_id}/watchlist/`);
    return {
        type: ADD_TO_WATCHLIST,
        payload: request
    }
}

export function removeFromWatchlist(movie_id) {
    const request = axios.delete(`${ROOT_URL}/api/movies/${movie_id}/watchlist/`);
    return {
        type: REMOVE_FROM_WATCHLIST,
        payload: request
    }
}

export function updateWatchlist(movie_id, action, type) {
    const path = `${ROOT_URL}/api/movies/${movie_id}/${action}/`;
    let request = null;
    if(type === 'PUT') request = axios.put(path);
    if(type === 'DELETE') request = axios.delete(path);

    return {
        type: UPDATE_WATCHLIST,
        payload: request
    };
}

export function rateMovie(movie_id, rating=null, type='PUT') {
    const path = `${ROOT_URL}/api/movies/${movie_id}/ratings/${rating}/`;
    let request = null;
    if(type === 'PUT') request = axios.put(path);
    if(type === 'DELETE') request = axios.delete(path);

    return {
        type: RATE_MOVIE,
        payload: request
    };
}

export function voteActor(role_id) {
    const request = axios.put(`${ROOT_URL}/api/roles/${role_id}/vote-up/`);
    return {
        type: VOTE_ACTOR,
        payload: request
    }
}
