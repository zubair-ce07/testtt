import axios from "axios";
import {loginEndpoint, registrationEndpoint} from "../Utils/constants";

export const loginAPI = data => {
    return axios.post(loginEndpoint, data)
};

export const registerAPI = data => {
    return axios.post(registrationEndpoint, data)
};
