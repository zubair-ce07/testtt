import axios from 'axios';
import { MYFACEBOOK_DOMAIN } from "../config"


export function LoginUser(props)
{
    const request = axios.post(`${MYFACEBOOK_DOMAIN}login/`, props);

    return {
        type: 'USER_LOGIN',
        payload: request
    };
}
