import axios from 'axios';

import {
    EXPLORE_WITH_DATE,
    EXPLORE_WITH_GENRE,
    GET_GENRES,
    REQUESTING_WITH_DATE,
    REQUESTING_WITH_GENRE,
    ROOT_URL,
    LOADING_MORE,
    LOADED_MORE
} from './action_types'


export function fetchReleasedOn(day, month, year) {
    const request = axios.get(`${ROOT_URL}/api/movies/released-on/?day=${day}&month=${month}&year=${year}`);
    return {
        type: EXPLORE_WITH_DATE,
        payload: request
    };
}

export function requestingWithReleaseDate() {
    return {
        type: REQUESTING_WITH_DATE,
        payload: 'fetching'
    }
}

export function fetchGenreMovies(genre_id) {
    const request = axios.get(`${ROOT_URL}/api/genres/${genre_id}/movies/?limit=3`);
    return {
        type: EXPLORE_WITH_GENRE,
        payload: request
    };
}

export function requestingWithGenre() {
    return {
        type: REQUESTING_WITH_GENRE,
        payload: 'fetching'
    }
}

export function loadingMore() {
    return {
        type: LOADING_MORE,
        payload: 'fetching'
    }
}

export function fetchMore(next_page) {
    const request = axios.get(next_page);
    return {
        type: LOADED_MORE,
        payload: request
    };
}

export function fetchGenres() {
    const request = axios.get(`${ROOT_URL}/api/genres/`);
    return {
        type: GET_GENRES,
        payload: request
    };
}

