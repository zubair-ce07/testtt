import axios from 'axios';
import { SEARCH_USERS } from "../config"


export function changeSearchPage(pageRequest)
{
    const request = axios({
        method:'get',
        url: pageRequest,
        headers: {'Authorization': `Token ${localStorage.getItem('token')}`}
    });

    return {
        type: SEARCH_USERS,
        payload: request
    };
}