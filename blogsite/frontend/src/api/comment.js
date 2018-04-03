import axios from 'axios';
import {baseUrl} from '../api/config'
axios.defaults.headers.common['Authorization'] = 'apple';
class commentApi {

    static getComments(postId) {
        var url=`${baseUrl}posts/${postId}/comments`;
        return fetch(url, {
            headers: { 'Authorization': 'apple' }
        }).then(response => {
            return response.json();
        }).catch(error => {
            return error;
        });
    }
    static deleteComment(commentId) {
        var url=`${baseUrl}comments/${commentId}`;

        return axios.delete(url)
            .then(response => {
                return response.data;
            }).catch(error => {
                return error;
            });
    }
    static addComment( comment) {
        var url=`${baseUrl}comments`;

        return axios.post(url, comment)
            .then(response => {
                return response.data;
            }).catch(error => {
                return error;
            });
    }
    static updateComment(comment,commentId) {
        var url=`${baseUrl}comments/${commentId}`;

        return axios.put(url, comment)
            .then(response => {
                return response.data;
            }).catch(error => {
                return error;
            });
    }
}

export default commentApi;
