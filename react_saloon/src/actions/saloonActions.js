import axios from 'axios';
import ls from 'local-storage';
import { REACT_APP_API_ENDPOINT_BASE_URL } from '../constants/config';

export const fetchSaloons = () => {

    return dispatch => {
        return axios.get(REACT_APP_API_ENDPOINT_BASE_URL+'shop/api/saloons/').then((response) => {
            dispatch({ type: 'FETCH_SALOON_SUCESSFUL', payload: response.data });
        }).catch(() => {
            dispatch({ type: 'FETCH_SALOON_FAILED' });
        });
    };

};

export const saloon_profile = () => {

    return dispatch => {
        const AuthStr = 'Token '.concat(ls.get('token'));
        return axios.get(REACT_APP_API_ENDPOINT_BASE_URL+'shop/api/profile/', { headers: { Authorization: AuthStr } }).then((response) => {
            dispatch({ type: 'SALOON_PROFILE_SUCESSFUL', payload: response.data });
        }).catch(() => {
            dispatch({ type: 'SALOON_PROFILE_FAILED' });
        });
    };

};

export const add_time_slots = (data) => {
    return dispatch => {
        const AuthStr = 'Token '.concat(ls.get('token'));
        return axios.post(REACT_APP_API_ENDPOINT_BASE_URL+'shop/api/mysaloon/', data, { headers: { Authorization: AuthStr } }).then((response) => {
            console.log(response);
            dispatch({ type: 'ADD_SLOTS_SUCESSFUL', payload: response.data });
        }).catch((err) => {
            console.log(err.response);
            dispatch({ type: 'ADD_SLOTS_FAILED' });
        });
    };

};

export const get_time_slots = () => {
    return dispatch => {
        const AuthStr = 'Token '.concat(ls.get('token'));
        return axios.get(REACT_APP_API_ENDPOINT_BASE_URL+'shop/api/mysaloon/', { headers: { Authorization: AuthStr } }).then((response) => {
            dispatch({ type: 'GET_SLOTS_SUCESSFUL', payload: response.data });
        }).catch(() => {
            dispatch({ type: 'GET_SLOTS_FAILED' });
        });
    };

};

export const get_time_slots_for_user = (shop_name) => {
    return dispatch => {
        const AuthStr = 'Token '.concat(ls.get('token'));
        return axios.get(REACT_APP_API_ENDPOINT_BASE_URL+'shop/api/shop/' + shop_name, { headers: { Authorization: AuthStr } }).then((response) => {
            dispatch({ type: 'GET_SLOTS_FOR_USER_SUCESSFUL', payload: response.data });
        }).catch(() => {
            dispatch({ type: 'GET_SLOTS_FOR_USER_FAILED' });
        });
    };

};

export const get_reservations_for_user = () => {
    return dispatch => {
        const AuthStr = 'Token '.concat(ls.get('token'));
        return axios.get(REACT_APP_API_ENDPOINT_BASE_URL+'customer/api/myreservations/', { headers: { Authorization: AuthStr } }).then((response) => {
            console.log(response);
            dispatch({ type: 'GET_RESERVATION_FOR_USER_SUCESSFUL', payload: response.data });
        }).catch((err) => {
            console.log(err.response);
            dispatch({ type: 'GET_RESERVATION_FOR_USER_FAILED' });
        });
    };

};

export const get_saloon_reservations = () => {
    return dispatch => {
        const AuthStr = 'Token '.concat(ls.get('token'));
        return axios.get(REACT_APP_API_ENDPOINT_BASE_URL+'shop/api/myreservations/', { headers: { Authorization: AuthStr } }).then((response) => {
            dispatch({ type: 'GET_SALOON_RESERVATION_SUCESSFUL', payload: response.data });
        }).catch(() => {
            dispatch({ type: 'GET_SALOON_RESERVATION_FAILED' });
        });
    };

};

export const reserve_slot_for_user = (time_slot) => {
    return dispatch => {
        const AuthStr = 'Token '.concat(ls.get('token'));
        return axios.post(REACT_APP_API_ENDPOINT_BASE_URL+'shop/api/reserve_slot/', { time_slot }, { headers: { Authorization: AuthStr } }).then((response) => {
            console.log(response);
            dispatch({ type: 'SLOTS_RESERVED_SUCESSFUL', time_slot });
        }).catch(() => {
            dispatch({ type: 'SLOTS_RESERVED_FAILED' });
        });
    };

};

export const cancel_reservation = (id) => {
    return dispatch => {
        const AuthStr = 'Token '.concat(ls.get('token'));
        return axios.delete(REACT_APP_API_ENDPOINT_BASE_URL+'shop/api/cancel-reservation/' + id, { headers: { Authorization: AuthStr } }).then(() => {
            dispatch({ type: 'DELETE_RESERVATION_SUCESSFUL', id });
        }).catch(() => {
            dispatch({ type: 'DELETE_SALOON_RESERVATION_FAILED' });
        });
    };
};

export const update_saloon_profile = (data) => {
    const request_data = {
        'user': {},
        'phone_no': data.phone_no,
        'address': data.address
    };
    request_data['user'] = {
        'first_name': data.first_name,
        'last_name': data.last_name,
        'email': data.email,
        'username': data.username
    };
    return dispatch => {
        const AuthStr = 'Token '.concat(ls.get('token'));
        return axios.post(REACT_APP_API_ENDPOINT_BASE_URL+'shop/api/profile/', request_data, { headers: { Authorization: AuthStr } }).then((response) => {
            console.log(response);
            dispatch({ type: 'SALOON_UPDATE_PROFILE_SUCESSFUL', payload: response.data });
        }).catch((err) => {
            console.log(err.response);
            dispatch({ type: 'SALOON_UPDATE_PROFILE_FAILED' });
        });
    };

};