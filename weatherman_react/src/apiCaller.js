import axios from "axios";
import * as constants from "./constants";


export const get = (url) =>{
    return axios.get(constants.BASE_URL + url)
        .then(function (response) {
            return response.data
        })
        .catch(function (error) {
            console.log(error);
            throw error;
        })
}