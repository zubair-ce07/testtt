export const userProfileEndpoint = 'http://localhost:8000/api/users/6/';
export const groupJoinEndpoint = 'http://localhost:8000/api/users/6/group-join/';
export const friendListEndpoint = 'http://localhost:8000/api/users/6/friends/';
export const prependDomain = link =>  `http://localhost:8000${link}`;

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
