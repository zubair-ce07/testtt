import axios from 'axios';
import { DELETE_BLOG_POST, ROOT_URL, API_KEY } from "../config"

export function deleteBlog(blogId)
{
    const request = axios.delete(`${ROOT_URL}${blogId}`);

    return {
        type: DELETE_BLOG_POST,
        payload: request
    }
}