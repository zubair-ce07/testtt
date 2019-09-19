import axios from 'axios';
import ls from 'local-storage';
import { REACT_APP_API_ENDPOINT_BASE_URL } from '../constants/config';
import {CUSTOMER_PROFILE_SUCCESSFUL,CUSTOMER_PROFILE_FAILED,
    CUSTOMER_UPDATE_PROFILE_SUCCESSFUL,
    CUSTOMER_UPDATE_PROFILE_FAILED} from '../constants/actionsTypeConstants';


export const customer_profile = () => {
    
    return dispatch => {
        const AuthStr = 'Token '.concat(ls.get('token'));
        return axios.get(REACT_APP_API_ENDPOINT_BASE_URL+'customer/api/profile/', { headers: { Authorization: AuthStr } }).then((response) => {
            dispatch({ type: CUSTOMER_PROFILE_SUCCESSFUL, payload: response.data });
        }).catch(() => {
            dispatch({ type: CUSTOMER_PROFILE_FAILED });
        });
    };

};

export const update_customer_profile = (data) => {
    const request_data = {
        'user': {},
        'phone_no': data.phone_no
    };
    request_data['user'] = {
        'first_name': data.first_name,
        'last_name': data.last_name,
        'email': data.email,
        'username': data.username
    };

    return dispatch => {
        const AuthStr = 'Token '.concat(ls.get('token'));
        return axios.post(REACT_APP_API_ENDPOINT_BASE_URL+'customer/api/profile/', request_data, { headers: { Authorization: AuthStr } }).then((response) => {
            dispatch({ type: CUSTOMER_UPDATE_PROFILE_SUCCESSFUL, payload: response.data });
        }).catch(() => {
            dispatch({ type: CUSTOMER_UPDATE_PROFILE_FAILED });
        });
    };

};