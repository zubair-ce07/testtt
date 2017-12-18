import axios from 'axios';

import {FETCH_MOVIE_DETAIL, FETCHING_MOVIE, ROOT_URL} from './action_types'


export function fetchMovieDetail(movie_id) {
    const request = axios.get(`${ROOT_URL}/api/movies/${movie_id}/?include=images,cast,crew,videos`);
    return {
        type: FETCH_MOVIE_DETAIL,
        payload: request
    };
}

export function fetchingMovie(){
    return {
        type: FETCHING_MOVIE,
        payload: 'fetching'
    };
}
