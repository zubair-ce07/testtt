import axios from 'axios';

import {FETCH_ACTIVITIES, ROOT_URL} from './action_types'


export function fetchActivities() {
    const request = axios.get(`${ROOT_URL}/api/activities/`);

    return {
        type: FETCH_ACTIVITIES,
        payload: request
    };
}
