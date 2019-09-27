import React from 'react';
import Typography from "@material-ui/core/Typography";

export const fetchCommentsUrl = post => {
    return 'http://localhost:8000/api/posts/' + post.id + '/comments/'
};
export const deleteCommentUrl = comment => {
    return 'http://localhost:8000/api/posts/comments/' + comment.id + '/'
};
export const createCommentUrl = post => {
    return 'http://localhost:8000/api/posts/' + post.id + '/comments/'
};
export const deletePostUrl = post => {
    return 'http://localhost:8000/api/posts/' + post.id + '/'
};
export const fetchCreatePostsUrl = 'http://localhost:8000/api/posts/';
export const fetchCreateUpvoteUrl = post => {
    return 'http://localhost:8000/api/posts/' + post.id + '/upvotes/'
};
export const deleteUpvoteUrl = (post, user) => {
    return 'http://localhost:8000/api/posts/' + post.id + '/upvotes/' + user + '/'
};
export const fetchCreateDownvoteUrl = post => {
    return 'http://localhost:8000/api/posts/' + post.id + '/downvotes/'
};
export const deleteDownvoteUrl = (post, user) => {
    return 'http://localhost:8000/api/posts/' + post.id + '/downvotes/' + user + '/'
};
export const userprofileEndpoint = 'http://localhost:8000/api/users/2/';
export const groupJoinEndpoint = 'http://localhost:8000/api/users/2/group-join/';
export const friendListEndpoint = 'http://localhost:8000/api/users/2/friends/';
export const prependDomain = link => {
    return 'http://localhost:8000' + link
};

export const Copyright = () => {
    return (
        <Typography variant="body2" color="textSecondary" align="center">
            {'Copyright © '}
            Social App
            {new Date().getFullYear()}
            {'.'}
        </Typography>
    );
};

export const loginEndpoint = 'http://localhost:8000/api/users/rest-auth/login/';
export const registrationEndpoint = 'http://localhost:8000/api/users/';
export const logoutEndpoint = 'http://localhost:8000/api/users/rest-auth/logout/';
