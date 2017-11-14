import axios from 'axios';
import { FETCH_BLOG_POSTS, ROOT_URL, API_KEY } from "../config"

export function fetchBlogPosts()
{
    const request = axios.get(ROOT_URL);

    return {
        type: FETCH_BLOG_POSTS,
        payload: request
    }
}