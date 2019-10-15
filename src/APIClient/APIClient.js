import axios from "axios";
import {
    createCommentUrl,
    deleteCommentUrl,
    deletePostUrl,
    fetchCommentsUrl, fetchCreateUpvoteUrl,
    fetchCreatePostsUrl, deleteUpvoteUrl, fetchCreateDownvoteUrl, deleteDownvoteUrl
} from "../Utils/constants";


export const fetchCommentsDB = post => {
    return axios.get(fetchCommentsUrl(post));
};

export const createCommentDB = (post, data) => {
    return axios.post(createCommentUrl(post), data)
};

export const deleteCommentDB = comment => {
    return axios.delete(deleteCommentUrl(comment));
};

export const fetchPostsDB = () => {
    return axios.get(fetchCreatePostsUrl)
};

export const createPostDB = data => {
    return axios.post(fetchCreatePostsUrl, data)
};

export const deletePostDB = post => {
    return axios.delete(deletePostUrl(post))
};

export const fetchUpvotesDB = post => {
    return axios.get(fetchCreateUpvoteUrl(post))
};

export const createUpvoteDB = (post, data) => {
    return axios.post(fetchCreateUpvoteUrl(post), data)
};

export const deleteUpvoteDB = (post, user) => {
    return axios.delete(deleteUpvoteUrl(post, user))
};

export const fetchDownVotesDB = post => {
    return axios.get(fetchCreateDownvoteUrl(post))
};

export const createDownvotevoteDB = (post, data) => {
    return axios.post(fetchCreateDownvoteUrl(post), data)
};

export const deleteDownvoteDB = (post, user) => {
    return axios.delete(deleteDownvoteUrl(post, user))
};
