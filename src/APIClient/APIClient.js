import axios from "axios";
import {login_endpoint, registration_endpoint} from "../Utils/constants";

export const loginAPI = data => {
    return axios.post(login_endpoint, data)
};

export const registerAPI = data => {
    return axios.post(registration_endpoint, data)
};
