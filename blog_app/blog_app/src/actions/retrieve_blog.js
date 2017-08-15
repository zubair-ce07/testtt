import axios from 'axios';
import { FETCH_BLOG, ROOT_URL } from "../config"

export function fetchBlog(blogId)
{
    const request = axios.get(ROOT_URL + blogId);

    return {
        type: FETCH_BLOG,
        payload: request
    }
}