import axios from 'axios';
import { MYFACEBOOK_DOMAIN } from "../config"


export function RetrieveNews()
{
    const request = axios({
        method:'get',
        url: `${MYFACEBOOK_DOMAIN}news/`,
        headers: {'Authorization': `Token ${localStorage.getItem('token')}`}
    });

    return {
        type: 'NEWS_LIST',
        payload: request
    };
}
