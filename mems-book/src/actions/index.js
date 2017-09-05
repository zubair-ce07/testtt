import axios from 'axios'
import {LOGIN_ACTION, SIGNUP_ACTION, API_LOGIN_URL, GET_USERS_MEMS,
    API_SIGNUP_URL, DISPLAY_LOGIN_TAB, DISPLAY_SIGUP_TAB,API_USERS_MEMS_URL,
    API_PUBLIC_MEMS_URL, GET_PUBLIC_MEMS, API_USER_ACTIVITIES_URL,
    GET_USER_ACTIVITIES, API_LOGOUT_URL, LOGOUT_ACTION, GET_USER_PROFILE,
    API_USER_PROFILE_URL, ADD_CATEGORY, API_ADD_CATEGORY_URL, GET_CATEGORIES,
    API_GET_CATEGORIES_URL, ADD_MEM, API_MEMS_URL, UPDATE_PROFILE, DELETE_MEM, GET_MEM} from '../constants';


export const Login = function (credentials) {
    return {
        type:  LOGIN_ACTION,
        payload: axios.post(API_LOGIN_URL,credentials)
    };
};
export const logout = function (token) {
    return {
        type: LOGOUT_ACTION ,
        payload: axios.post(API_LOGOUT_URL,{},{headers:{Authorization: 'Token '+token }})
    };
};
export const signup = function (user) {
    console.log(user);
    return {
        type:  SIGNUP_ACTION,
        payload: axios.post(API_SIGNUP_URL,user)
    };
};
export const getUserMems = function (token) {
    return {
        type: GET_USERS_MEMS ,
        payload: axios.get(API_USERS_MEMS_URL,{headers:{'Authorization': 'Token '+token }})
    }
};
export const getPublicMems = function (token) {
    return {
        type: GET_PUBLIC_MEMS ,
        payload: axios.get(API_PUBLIC_MEMS_URL,{headers:{'Authorization': 'Token '+token }})
    }
};
export const getUserActivities = function (token) {
    return {
        type: GET_USER_ACTIVITIES ,
        payload: axios.get(API_USER_ACTIVITIES_URL,{headers:{'Authorization': 'Token '+token }})
    }
};
export const getUserProfile = function (user_id, token) {
    return {
        type: GET_USER_PROFILE ,
        payload: axios.get(API_USER_PROFILE_URL+user_id+'/',{headers:{'Authorization': 'Token '+token }})
    }
};
export const addCategory = function (category, token) {
    return {
        type: ADD_CATEGORY ,
        payload: axios.post(API_ADD_CATEGORY_URL,category, {headers:{'Authorization': 'Token '+token }})
    }
};
export const getMem = function (id, token) {
    return {
        type: GET_MEM ,
        payload: axios.get(API_MEMS_URL+id+'/', {headers:{'Authorization': 'Token '+token}})
    }
};
export const addMem = function (mem, token) {
    return {
        type: ADD_MEM ,
        payload: axios.post(API_MEMS_URL,mem, {headers:{'Authorization': 'Token '+token,
            'Content-Type': 'multipart/form-data'}})
    }
};
export const editMem = function (mem,id,token) {
    return {
        type: ADD_MEM ,
        payload: axios.put(API_MEMS_URL+id+'/',mem, {headers:{'Authorization': 'Token '+token,
            'Content-Type': 'multipart/form-data'}})
    }
};
export const deleteMem = function (id, token) {
     return {
        type: DELETE_MEM ,
         id : id, // to keep record of deleted object
        payload: axios.delete(API_MEMS_URL+id+'/', {headers:{'Authorization': 'Token '+token}})
    }
};


export const getCategories = function (token) {
    return {
        type: GET_CATEGORIES ,
        payload: axios.get(API_GET_CATEGORIES_URL,{headers:{'Authorization': 'Token '+token }})
    }
};

export const updateProfile = function (user, id, token){
    return {
        type: UPDATE_PROFILE ,
        payload: axios.put(API_USER_PROFILE_URL+id+'/',user,{headers:{'Authorization': 'Token '+token,
            'Content-Type': 'multipart/form-data'}})
    }
}
export const LoginClick = function() {
    return {
        type: DISPLAY_LOGIN_TAB,
        payload: 'login'
    };
};

export const SignUpClick = function() {
    return {
        type: DISPLAY_SIGUP_TAB,
        payload: 'signup'
    };
};
