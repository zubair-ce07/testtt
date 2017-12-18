import axios from 'axios';

import {
    ADD_TO_WATCHLIST,
    REMOVE_FROM_WATCHLIST,
    GET_WATCHLIST,
    VOTE_ACTOR,
    UPDATE_WATCHLIST,
    RATE_MOVIE,
    ROOT_URL,
    FETCHING_WATCHLIST
} from './action_types';


export function fetchWatchList(filter) {
    return dispatch => {
        dispatch({type: FETCHING_WATCHLIST});
        const request = axios.get(`${ROOT_URL}/api/${filter}/?limit=3`);
        dispatch({
           type: GET_WATCHLIST,
            payload: request
        });
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
