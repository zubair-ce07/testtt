import axios from 'axios';
import setAuthorizationToken from '../utils/setAuthorizationToken';
import {SET_CURRENT_USER, ROOT_URL} from './action_types';


export function setCurrentUser(user) {
    return {
        type: SET_CURRENT_USER,
        user
    };
}

export function logout() {
    return dispatch => {
        localStorage.removeItem('user');
        setAuthorizationToken(false);
        dispatch(setCurrentUser({}));
    }
}

export function login(data) {
    return dispatch => {
        return axios.post(`${ROOT_URL}/api/authenticate/`, data).then(res => {
            localStorage.setItem('user', JSON.stringify(res.data));
            setAuthorizationToken(res.data.token);
            dispatch(setCurrentUser(res.data));
        });
    }
}
