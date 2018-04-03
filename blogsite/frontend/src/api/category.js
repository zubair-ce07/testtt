import axios from 'axios';
import {baseUrl} from '../api/config'
axios.defaults.headers.common['Authorization'] = 'apple';
class categoryApi {

    static getCategoryData() {
        var url=`${baseUrl}categories`;
        return axios.get(url)
            .then(response => {
                return response.data;
            }).catch(error => {
                return error;
            });
    }
    static getPostsOfCategory(category) {
        var url=`${baseUrl}${category}/posts`;
        return axios.get(url)
            .then(response => {
                return response.data;
            }).catch(error => {
                return error;
            })
    }

}

export default categoryApi;
