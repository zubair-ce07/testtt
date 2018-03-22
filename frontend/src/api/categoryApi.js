import axios from 'axios';
axios.defaults.headers.common['Authorization'] = 'apple';
class categoryApi {

    static getCategoryData() {
        var url='http://localhost:3001/categories';
        return fetch(url, {
            headers: { 'Authorization': 'apple' }
        }).then(response => {
            return response.json();
        }).catch(error => {
            return error;
        });
    }

    static getPostsData(category) {
        var url=`http://localhost:3001/${category}/posts`;
        return fetch(url, {
            headers: { 'Authorization': 'apple' }
        }).then(response => {
            return response.json();
        }).catch(error => {
            return error;
        });
    }
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
    static getComments(postId) {
        var url=`http://localhost:3001/posts/${postId}/comments`;
        return fetch(url, {
            headers: { 'Authorization': 'apple' }
        }).then(response => {
            return response.json();
        }).catch(error => {
            return error;
        });
    }
    static deleteComment(commentId) {
        var url=`http://localhost:3001/comments/${commentId}`;

       return axios.delete(url)
            .then(response => {
                console.log(response)
                return response.data;
            }).catch(error => {
            return error;
        });
    }
    static addComment( comment) {
        var url=`http://localhost:3001/comments`;

       return axios.post(url, comment)
            .then(response => {
                console.log(response)
                return response.data;
            }).catch(error => {
            return error;
        });
    }
    static editComment(commentId, comment) {
        var url=`http://localhost:3001/comments/${commentId}`;

       return axios.put(url, comment)
            .then(response => {
                console.log(response)
                return response.data;
            }).catch(error => {
            return error;
        });
    }
}

export default categoryApi;
