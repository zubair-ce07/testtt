import axios from 'axios';


export const FETCH_NEWS_DETAIL = 'fetch_news_detail';
export const FETCH_NEWS_TOP = 'fetch_news_top';
export const FETCH_NEWS_CATEGORIES = 'fetch_news_categories';
export const FETCH_SEARCH_NEWS = 'fetch_search_news';
export const LOGIN_USER = 'login_user';
export const SIGNUP_USER = 'signup_user';
export const FETCH_NEWS_BY_CATEGORY_NAME = 'fetch_news_by_category_name';
export const PROFILE_USER = 'profile_user';
export const INTERESTS_USER = 'interests_user';
export const ALL_CATEGORIES = 'all_categories';
export const UPDATE_INTERESTS = 'update_user_interests';
export const UPDATE_USER_PROFILE = 'update_user_profile';

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

export function fetchCategoryNews(categoryName) {
  const request = axios.get(`${ROOT_URL}/v1/categories/${categoryName}/news`);

  return {
      type: FETCH_NEWS_BY_CATEGORY_NAME,
      payload: request
  }
}

export function userProfile(token){
    const request = axios.get(`${ROOT_URL}/v1/users/profile/`,{
        headers : { Authorization : `Token ${token}`}
    });
    
    return {
        type: PROFILE_USER,
        payload: request,
    };
}

export function userCategories(token){
    const request = axios.get(`${ROOT_URL}/v1/users/interests/`,{
        headers : { Authorization : `Token ${token}`}
    });
    
    return {
        type: INTERESTS_USER,
        payload: request,
    };
}

export function allCategories(){
    const request = axios.get(`${ROOT_URL}/v1/categories/`);
    
    return {
        type: ALL_CATEGORIES,
        payload: request,
    };
}

export function updateUserInterests(token, interests){
    console.log("Update Token Action", token)
    const config = {
        headers : { Authorization : `Token ${token}`}
    }
    const params = { interests };
    const request = axios.post(`${ROOT_URL}/v1/users/interests/`, params, config);
    
    return {
        type: UPDATE_INTERESTS,
        payload: request,
    };
}

export function updateUserProfile(token, data){
    const config = {
        headers : { Authorization : `Token ${token}`}
    }
    const params = data;
    const request = axios.post(`${ROOT_URL}/v1/users/profile/`, params, config);
    
    return {
        type: UPDATE_USER_PROFILE,
        payload: request,
    };
}