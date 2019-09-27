import axios from "axios";
import {
    createCommentUrl,
    deleteCommentUrl,
    deleteDownvoteUrl,
    deletePostUrl,
    deleteUpvoteUrl,
    fetchCommentsUrl,
    fetchCreateDownvoteUrl,
    fetchCreatePostsUrl,
    fetchCreateUpvoteUrl,
    friendListEndpoint,
    groupJoinEndpoint,
    loginEndpoint,
    logoutEndpoint,
    prependDomain,
    registrationEndpoint,
    userprofileEndpoint
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

export const UserProfileAPI = () => {
    return axios.get(userprofileEndpoint)
};

export const GroupDataAPI = () => {
    return axios.get(groupJoinEndpoint)
};

export const WorkInformationAPI = link => {
    return axios.get(prependDomain(link))
};

export const AcademicInformationAPI = link => {
    return axios.get(prependDomain(link))
};

export const FriendListAPI = () => {
    return axios.get(friendListEndpoint)
};

export const loginAPI = data => {
    return axios.post(loginEndpoint, data)
};

export const registerAPI = data => {
    return axios.post(registrationEndpoint, data)
};

export const logoutAPI = () => {
    return axios.post(logoutEndpoint, {})
};