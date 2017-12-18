import _ from 'lodash';
import axios from 'axios';

import {ROOT_URL, FETCH_USER, SEND_FOLLOW_REQUEST, GET_NETWORK, FETCHING_NETWORK} from './action_types';
import {setCurrentUser} from './auth_actions';
import setAuthorizationToken from '../utils/setAuthorizationToken';


export function signupUser(data) {
    return dispatch => {
        const form = new FormData();
        _.map(data, (value, key) => {
            if(key === 'date_of_birth') form.append(key, value.toISOString().substring(0, 10));
            else if(key === 'photo') form.append(key, value[0]);
            else form.append(key, value);
        });
        return axios.post(`${ROOT_URL}/api/users/`, form).then(res => {
            localStorage.setItem('user', JSON.stringify(res.data));
            setAuthorizationToken(res.data.token);
            dispatch(setCurrentUser(res.data));
        });
    }
}

export function updateUser(data, user_id) {
    return dispatch => {
        const form = new FormData();
        if(data.photo && data.photo.length > 0) form.append('photo', data.photo[0]);
        if(data.password) form.append('password', data.password);
        return axios.patch(`${ROOT_URL}/api/users/${user_id}/`, form).then(res => {
            localStorage.setItem('user', JSON.stringify(res.data));
            dispatch(setCurrentUser(res.data));
        });
    }
}

export function fetchUser(user_id) {
    const request = axios.get(`${ROOT_URL}/api/users/${user_id}/`);

    return {
        type: FETCH_USER,
        payload: request
    };
}

export function sendFollowRequest(receiver_id) {
    const request = axios.put(`${ROOT_URL}/api/users/${receiver_id}/send-request/`);

    return {
        type: SEND_FOLLOW_REQUEST,
        payload: request
    };
}

export function fetchNetwork(type) {
    return dispatch => {
        dispatch({type: FETCHING_NETWORK});
        const request = axios.get(`${ROOT_URL}/api/${type}/?limit=3`);
        dispatch({
           type: GET_NETWORK,
            payload: request
        });
    };
}
