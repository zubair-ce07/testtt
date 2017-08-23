import axios from 'axios';
import { TRAINING_BASE_URL, SEARCH_USERS } from "../config"


export function searchUsers(query)
{
    const request = axios({
        method:'get',
        url: `${TRAINING_BASE_URL}search/?q=${query}`,
        headers: {'Authorization': `Token ${localStorage.getItem('token')}`}
    });

    return {
        type: SEARCH_USERS,
        payload: request
    };
}