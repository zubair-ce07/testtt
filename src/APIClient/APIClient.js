import axios from "axios"
import {
    createcomment_url,
    deletecomment_url,
    deletepost_url,
    fetchcomments_url, fetchcreateupvote_url,
    fetchcreateposts_url, deleteupvote_url, fetchcreatedownvote_url, deletedownvote_url
} from "../Utils/constants";


export const fetchCommentsDB = post => {
    return axios.get(fetchcomments_url(post));
};

export const createCommentDB = (post, data) => {
    return axios.post(createcomment_url(post), data)
};

export const deleteCommentDB = comment => {
    return axios.delete(deletecomment_url(comment));
};

export const fetchPostsDB = () => {
    return axios.get(fetchcreateposts_url)
};

export const createPostDB = data => {
    return axios.post(fetchcreateposts_url, data)
};

export const deletePostDB = post => {
    return axios.delete(deletepost_url(post))
};

export const fetchUpvotesDB = post => {
    return axios.get(fetchcreateupvote_url(post))
};

export const createUpvoteDB = (post, data) => {
    return axios.post(fetchcreateupvote_url(post), data)
};

export const deleteUpvoteDB = (post, user) => {
    return axios.delete(deleteupvote_url(post, user))
};

export const fetchDownVotesDB = post => {
    return axios.get(fetchcreatedownvote_url(post))
};

export const createDownvotevoteDB = (post, data) => {
    return axios.post(fetchcreatedownvote_url(post), data)
};

export const deleteDownvoteDB = (post, user) => {
    return axios.delete(deletedownvote_url(post, user))
};
