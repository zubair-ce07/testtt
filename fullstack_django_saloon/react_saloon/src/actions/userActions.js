import localStorage from 'local-storage';
import { getTokenHeader,makeApiUrl, makeGetCallWithHeader,makePostCall } from './utils';
import { REACT_APP_API_ENDPOINT_BASE_URL } from '../constants/config';
import { actionTypes } from '../constants/actionsTypeConstants';
import { apiEndPoints } from '../constants/apiEndPoints';
import { reactAppConstants } from '../constants/constants';
import { routeConstants } from '../constants/routeConstants';

export const login = (username, password) =>
    dispatch =>
        makePostCall(makeApiUrl(REACT_APP_API_ENDPOINT_BASE_URL,apiEndPoints.API_LOGIN), { username, password }).then((response) => {
            localStorage.set(reactAppConstants.USERNAME, response.data.user.username);
            localStorage.set(reactAppConstants.EMAIL, response.data.user.email);
            localStorage.set(reactAppConstants.TOKEN, response.data.token);
            localStorage.set(reactAppConstants.USER_TYPE, response.data.user_type);
            dispatch({ type: actionTypes.LOGIN_SUCCESSFUL, payload: response.data });
            return response;
        }).catch((err) => {
            dispatch({ type: actionTypes.LOGIN_FAILED });
            return err;
        });

export const logout = (history) =>
    dispatch =>
        makeGetCallWithHeader(makeApiUrl(REACT_APP_API_ENDPOINT_BASE_URL,apiEndPoints.API_LOGOUT), { headers: { [reactAppConstants.AUTHORIZATION]: getTokenHeader() } }).then((response) => {
            localStorage.clear();
            dispatch({ type: actionTypes.LOGOUT_SUCCESSFUL });
            history.push(routeConstants.LOGIN_ROUTE);
            return response;
        }).catch((err) => {
            dispatch({ type: actionTypes.LOGOUT_FAILED });
            return err;
        });

export const signup = (username, email, password1, password2, user_type) =>
    dispatch =>
        makePostCall(makeApiUrl(REACT_APP_API_ENDPOINT_BASE_URL,apiEndPoints.API_REGISTER), { username, email, password1, password2, user_type }).then((response) => {
            dispatch({ type: actionTypes.SIGNUP_SUCCESSFUL, payload: response.data });
            return response;
        }).catch((err) => {
            dispatch({ type: actionTypes.SIGNUP_FAILED });
            return err;
        });

export const userValueUpdate = (key, value) =>
    dispatch =>
        dispatch({ type: actionTypes.USER_VALUE_UPDATE, payload: { key, value } });