import axios from 'axios';
import ls from 'local-storage';
import { REACT_APP_API_ENDPOINT_BASE_URL } from '../constants/config';

export const login = (username, password) => {
    return dispatch => {
        return axios.post(REACT_APP_API_ENDPOINT_BASE_URL+'api/login/', { username, password }).then((response) => {
            ls.set('username', response.data.user.username);
            ls.set('email', response.data.user.email);
            ls.set('token', response.data.token);
            ls.set('user_type', response.data.user_type);
            dispatch({ type: 'LOGIN_SUCESSFUL', payload: response.data });
            return response;
        }).catch((err) => {
            dispatch({ type: 'LOGIN_FAILED' });
            return err;
        });
    };
};

export const logout = () => {
    return dispatch => {
        const AuthStr = 'Token '.concat(ls.get('token'));
        return axios.get(REACT_APP_API_ENDPOINT_BASE_URL+'api/logout/', { headers: { Authorization: AuthStr } }).then((response) => {
            ls.clear();
            dispatch({ type: 'LOGOUT_SUCESSFUL' });
            return response;
        }).catch((err) => {
            dispatch({ type: 'LOGOUT_FAILED' });
            return err;
        });
    };
};

export const signup = (username, email, password1, password2, user_type) => {
    return dispatch => {
        return axios.post(REACT_APP_API_ENDPOINT_BASE_URL+'api/register/', { username, email, password1, password2, user_type }).then((response) => {
            dispatch({ type: 'SIGNUP_SUCESSFUL', payload: response.data });
            return response;
        }).catch((err) => {
            console.log(err.response);
            dispatch({ type: 'SIGNUP_FAILED' });
            return err;
        });
    };
};

export const user_value_update = (key, value) => {
    return dispatch => {
        dispatch({ type: 'USER_VALUE_UPDATE', payload: { key, value } });
    };

};