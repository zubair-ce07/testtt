import axios from 'axios';
import { TRAINING_BASE_URL, USER_LOGIN } from "../config"


export function loginUser(props) {
    const request = axios.post(`${TRAINING_BASE_URL}login/`, props);

    return {
        type: USER_LOGIN,
        payload: request
    };
}