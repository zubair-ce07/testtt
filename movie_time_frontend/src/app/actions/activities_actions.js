import axios from 'axios';

import {FETCH_ACTIVITIES, FETCHING_ACTIVITIES, ROOT_URL, FETCH_USER_ACTIVITIES} from './action_types'


export function fetchActivities() {
    return dispatch => {
        dispatch({type: FETCHING_ACTIVITIES});
        const request = axios.get(`${ROOT_URL}/api/activities/?limit=3`);
        dispatch({
           type: FETCH_ACTIVITIES,
            payload: request
        });
    };
}

export function fetchUserActivities(user_id) {
    return dispatch => {
        dispatch({type: FETCHING_ACTIVITIES});
        const request = axios.get(`${ROOT_URL}/api/users/${user_id}/activities/?limit=3`);
        dispatch({
           type: FETCH_USER_ACTIVITIES,
            payload: request
        });
    };
}
