import axios from 'axios';
import { TRAINING_BASE_URL, USER_PROFILE } from "../config"


export function retrieveProfile()
{
    const request = axios({
        method:'get',
        url: `${TRAINING_BASE_URL}profile/`,
        headers: {'Authorization': `Token ${localStorage.getItem('token')}`}
    });

    return {
        type: USER_PROFILE,
        payload: request
    };
}