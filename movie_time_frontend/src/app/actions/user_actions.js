import _ from 'lodash';
import axios from 'axios';

import {ROOT_URL} from './action_types';
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
