import axios from 'axios';
import {baseUrl} from '../api/config';
axios.defaults.headers.common['Authorization'] = 'apple';

class postApi {

    static getAllPostsData() {
        var url=`${baseUrl}posts`;
        return fetch(url, {
            headers: { 'Authorization': 'apple' }
        }).then(response => {
            return response.json();
        }).catch(error => {
            return error;
        });
    }
    static getPost(postId) {
        var url=`${baseUrl}posts/${postId}`;
        return fetch(url, {
            headers: { 'Authorization': 'apple' }
        }).then(response => {
            return response.json();
        }).catch(error => {
            return error;
        });
    }
    static addPost( post) {
        var url=`${baseUrl}posts`;

        return axios.post(url, post)
            .then(response => {
                return response.data;
            }).catch(error => {
                return error;
            });
    }
    static editPost( post, postId) {
        var url=`${baseUrl}posts/${postId}`;

        return axios.put(url, post)
            .then(response => {
                return response.data;
            }).catch(error => {
                return error;
            });
    }
    static deletePost(postId) {
        var url=`${baseUrl}posts/${postId}`;

        return axios.delete(url)
            .then(response => {
                return response.data;
            }).catch(error => {
                return error;
            });
    }

}export default postApi;