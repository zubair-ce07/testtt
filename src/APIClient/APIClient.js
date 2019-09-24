import axios from "axios"


export const deleteCommentDB = comment => {
    return axios.delete('http://localhost:8000/api/posts/comments/' + comment.id + '/');
};

export const fetchCommentsFromDB = post => {
    return axios.get('http://localhost:8000/api/posts/' + post.id + '/comments/');
};

export const createCommentDB = (post, data) => {
    return axios.post('http://localhost:8000/api/posts/' + post.id + '/comments/', data)
};

export const deletePostDB = post => {
    return axios.delete('http://localhost:8000/api/posts/' + post.id + '/')
};

export const fetchPostsDB = () => {
    return axios.get('http://localhost:8000/api/posts/')
};

export const createPostDB = data => {
    return axios.post('http://localhost:8000/api/posts/', data)
};

export const fetchUpvotesDB = post => {
    return axios.get('http://localhost:8000/api/posts/' + post.id + '/upvotes/')
};

export const fetchDownVotesDB = post => {
    return axios.get('http://localhost:8000/api/posts/' + post.id + '/downvotes/')
};

export const createUpvoteDB = (post, data) => {
    return axios.post('http://localhost:8000/api/posts/' + post.id + '/upvotes/', data)
};

export const deleteUpvoteDB = (post, user) => {
    return axios.delete('http://localhost:8000/api/posts/' + post.id + '/upvotes/' + user + '/')
};

export const createDownvotevoteDB = (post, data) => {
    return axios.post('http://localhost:8000/api/posts/' + post.id + '/downvotes/', data)
};

export const deleteDownvoteDB = (post, user) => {
    return axios.delete('http://localhost:8000/api/posts/' + post.id + '/downvotes/' + user + '/')
};