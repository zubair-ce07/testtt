import axios from 'axios'
import ls from 'local-storage'

export const fetchSaloons = () => {

    return dispatch => {
        return axios.get('http://localhost:8000/shop/api/saloons/').then((response) => {
            dispatch({ type: 'FETCH_SALOON_SUCESSFUL', payload: response.data });
        }).catch((err) => {
            dispatch({ type: 'FETCH_SALOON_FAILED' });
        })
    }

}

export const saloon_profile = () => {

    return dispatch => {
        const AuthStr = 'Token '.concat(ls.get('token'));
        return axios.get('http://localhost:8000/shop/api/profile/', { headers: { Authorization: AuthStr } }).then((response) => {
            dispatch({ type: 'SALOON_PROFILE_SUCESSFUL', payload: response.data });
        }).catch((err) => {
            dispatch({ type: 'SALOON_PROFILE_FAILED' });
        })
    }

}

export const add_time_slots = (data) => {
    return dispatch => {
        const AuthStr = 'Token '.concat(ls.get('token'));
        return axios.post('http://localhost:8000/shop/api/mysaloon/', data, { headers: { Authorization: AuthStr } }).then((response) => {
            console.log(response)
            dispatch({ type: 'ADD_SLOTS_SUCESSFUL', payload: response.data });
        }).catch((err) => {
            console.log(err.response)
            dispatch({ type: 'ADD_SLOTS_FAILED' });
        })
    }

}

export const get_time_slots = () => {
    return dispatch => {
        const AuthStr = 'Token '.concat(ls.get('token'));
        return axios.get('http://localhost:8000/shop/api/mysaloon/', { headers: { Authorization: AuthStr } }).then((response) => {
            dispatch({ type: 'GET_SLOTS_SUCESSFUL', payload: response.data });
        }).catch((err) => {
            dispatch({ type: 'GET_SLOTS_FAILED' });
        })
    }

}

export const get_time_slots_for_user = (shop_name) => {
    return dispatch => {
        const AuthStr = 'Token '.concat(ls.get('token'));
        return axios.get('http://localhost:8000/shop/api/shop/' + shop_name, { headers: { Authorization: AuthStr } }).then((response) => {
            dispatch({ type: 'GET_SLOTS_FOR_USER_SUCESSFUL', payload: response.data });
        }).catch((err) => {
            dispatch({ type: 'GET_SLOTS_FOR_USER_FAILED' });
        })
    }

}

export const get_reservations_for_user = () => {
    return dispatch => {
        const AuthStr = 'Token '.concat(ls.get('token'));
        return axios.get('http://localhost:8000/customer/api/myreservations/', { headers: { Authorization: AuthStr } }).then((response) => {
            console.log(response)
            dispatch({ type: 'GET_RESERVATION_FOR_USER_SUCESSFUL', payload: response.data });
        }).catch((err) => {
            console.log(err.response)
            dispatch({ type: 'GET_RESERVATION_FOR_USER_FAILED' });
        })
    }

}

export const update_saloon_profile = (data) => {
    const request_data = {
        'user': {},
        'phone_no': data.phone_no,
        'address': data.address
    }
    request_data['user'] = {
        'first_name': data.first_name,
        'last_name': data.last_name,
        'email': data.email,
        'username': data.username
    }
    return dispatch => {
        const AuthStr = 'Token '.concat(ls.get('token'));
        return axios.post('http://localhost:8000/shop/api/profile/', request_data, { headers: { Authorization: AuthStr } }).then((response) => {
            console.log(response)
            dispatch({ type: 'SALOON_UPDATE_PROFILE_SUCESSFUL', payload: response.data });
        }).catch((err) => {
            console.log(err.response)
            dispatch({ type: 'SALOON_UPDATE_PROFILE_FAILED' });
        })
    }

}