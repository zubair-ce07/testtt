import axios from 'axios';

import {FETCH_NOTIFICATIONS, DELETE_NOTIFICATIONS, RESPOND_TO_FOLLOW_REQUEST, ROOT_URL} from './action_types'


export function fetchNotifications() {
    const request = axios.get(`${ROOT_URL}/api/notifications/`);

    return {
        type: FETCH_NOTIFICATIONS,
        payload: request
    };
}

export function deleteNotification(notification_id) {
    const request = axios.delete(`${ROOT_URL}/api/notifications/${notification_id}/`);

    return {
        type: DELETE_NOTIFICATIONS,
        payload: request
    };
}

export function respondToFollowRequest(follow_request_id, response) {
    const request = axios.put(`${ROOT_URL}/api/requests/${follow_request_id}/${response}/`);
    return {
        type: RESPOND_TO_FOLLOW_REQUEST,
        payload: request
    }
}
