import axios from 'axios';


export const FETCH_NEWS_DETAIL = 'fetch_news_detail';
export const FETCH_NEWS_TOP = 'fetch_news_top';
export const FETCH_NEWS_CATEGORIES = 'fetch_news_categories';
export const FETCH_SEARCH_NEWS = 'fetch_search_news';
export const LOGIN_USER = 'login_user';
export const SIGNUP_USER = 'signup_user';


const ROOT_URL = 'http://localhost:8000/api';

export function fetchNewsDetail(id) {
    const request = axios.get(`${ROOT_URL}/v1/news/${id}`);

    return {
        type: FETCH_NEWS_DETAIL,
        payload: request
    }
}

export function fetchNewsTop(limit) {
    const request = axios.get(`${ROOT_URL}/v1/news/top/?limit=${limit}`);

    return {
        type: FETCH_NEWS_TOP,
        payload: request
    }
}

export function fetchNewsByCategories(limit) {
    const request = axios.get(`${ROOT_URL}/v1/news/categories/?limit=${limit}`);

    return {
        type: FETCH_NEWS_CATEGORIES,
        payload: request
    }
}

export function fetchSearchNews(query){
    const request = axios.get(`${ROOT_URL}/v1/news/search/?query=${query}`);

    return {
        type: FETCH_SEARCH_NEWS,
        payload: request
    }
}

export function loginUser(data){
    const request = axios.post(`${ROOT_URL}/v1/users/authenticate/`,{
        username: data.email,
        password: data.password
    });
    
    return {
        type: LOGIN_USER,
        payload: request,
    };
}

export function signupUser(data){
    const request = axios.post(`${ROOT_URL}/v1/users/create/`,{
        username: data.email,
        password: data.password,
        email: data.email,
        first_name: data.first_name,
        last_name: data.last_name
    });

    return {
        type: SIGNUP_USER,
        payload: request
    }
}









