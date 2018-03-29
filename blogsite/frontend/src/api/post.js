import axios from 'axios';
axios.defaults.headers.common['Authorization'] = 'apple';
class postApi {

    static getAllPostsData() {
        var url=`http://localhost:3001/posts`;
        return fetch(url, {
            headers: { 'Authorization': 'apple' }
        }).then(response => {
            return response.json();
        }).catch(error => {
            return error;
        });
    }
    static getPost(postId) {
        var url=`http://localhost:3001/posts/${postId}`;
        return fetch(url, {
            headers: { 'Authorization': 'apple' }
        }).then(response => {
            return response.json();
        }).catch(error => {
            return error;
        });
    }
    static addPost( post) {
        var url='http://localhost:3001/posts';

        return axios.post(url, post)
            .then(response => {
                return response.data;
            }).catch(error => {
                return error;
            });
    }
    static editPost( post, postId) {
        var url=`http://localhost:3001/posts/${postId}`;

        return axios.put(url, post)
            .then(response => {
                return response.data;
            }).catch(error => {
                return error;
            });
    }
    static deletePost(postId) {
        var url=`http://localhost:3001/posts/${postId}`;

        return axios.delete(url)
            .then(response => {
                return response.data;
            }).catch(error => {
                return error;
            });
    }

}

export default postApi;
















