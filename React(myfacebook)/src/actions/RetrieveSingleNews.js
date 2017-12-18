import axios from 'axios';
import { MYFACEBOOK_DOMAIN } from "../config"


export function RetrieveSingleNews(news_id)
{
    const request = axios({
        method:'get',
        url: `${MYFACEBOOK_DOMAIN}news/`+news_id+'/',
        headers: {'Authorization': `Token ${localStorage.getItem('token')}`}
    });

    return {
        type: 'NEWS_DETAIL',
        payload: request
    };
}
