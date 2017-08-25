import axios from 'axios';
import TheMovieDatabase from 'themoviedatabase';

export const FETCH_MOVIES = 'FETCH_MOVIES';
export const FETCH_REVIEWS = 'FETCH_REVIEWS';
export const FETCH_MOVIE = 'FETCH_MOVIE';
export const FETCH_ACTOR = 'FETCH_ACTOR';
export const CREATE_REVIEW = 'CREATE_REVIEW';

const ROOT_URL = 'http://localhost:8000';
const MDB = new TheMovieDatabase('7b43db1b983b055bffd7534a06cafd6c');

export function fetchMovies(term) {
    const request = term === '' ? MDB.movies.nowPlaying() : MDB.search.movies({query: term});

    return {
        type: FETCH_MOVIES,
        payload: request
    };
}

export function fetchMovie(id) {
    const request = MDB.movies.details({append_to_response: "credits"}, {movie_id: id});

    return {
        type: FETCH_MOVIE,
        payload: request
    };
}

export function fetchActor(id) {
    const request = MDB.people.details(null, {person_id: id});

    return {
        type: FETCH_ACTOR,
        payload: request
    };
}

export function addReview(props, callback) {
    const request = axios.post(`${ROOT_URL}/reviews/`, props)
        .then(res => {
            callback();
            return res;
        });

    return {
        type: CREATE_REVIEW,
        payload: request
    };
}

export function fetchReviews(id) {
    const request = axios.get(`${ROOT_URL}/reviews/${id}`);

    return {
        type: FETCH_REVIEWS,
        payload: request
    };
}
