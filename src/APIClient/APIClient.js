import axios from "axios";

export const loginAPI = data => {
    return axios.post('http://localhost:8000/api/users/rest-auth/login/', data)
};

export const registerAPI = data => {
    return axios.post('http://localhost:8000/api/users/', data)
};
