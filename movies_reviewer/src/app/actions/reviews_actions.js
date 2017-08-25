import axios from 'axios';

export const FETCH_REVIEWS = 'FETCH_REVIEWS';
export const CREATE_REVIEW = 'CREATE_REVIEW';

const ROOT_URL = 'http://localhost:8000';

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
