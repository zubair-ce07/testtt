import axios from "axios";
import BASE_URL from "./config";


export const get = (url) =>{
    return axios.get(BASE_URL + url)
        .then(function (response) {
            return response.data
        })
        .catch(function (error) {
            console.log(error);
            throw error;
        })
}