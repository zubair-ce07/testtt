import axios from 'axios';
import { CREATE_BLOG_POST, ROOT_URL, API_KEY } from "../config"

export function createBlogPost(props)
{
    const request = axios.post(`${ROOT_URL}`, props);

    return {
        type: CREATE_BLOG_POST,
        payload: request
    }
}