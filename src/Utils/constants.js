export const fetchcomments_url = post => {
    return 'http://localhost:8000/api/posts/' + post.id + '/comments/'
};
export const deletecomment_url = comment => {
    return 'http://localhost:8000/api/posts/comments/' + comment.id + '/'
};
export const createcomment_url = post => {
    return 'http://localhost:8000/api/posts/' + post.id + '/comments/'
};
export const deletepost_url = post => {
    return 'http://localhost:8000/api/posts/' + post.id + '/'
};
export const fetchcreateposts_url = 'http://localhost:8000/api/posts/';
export const fetchcreateupvote_url = post => {
    return 'http://localhost:8000/api/posts/' + post.id + '/upvotes/'
};
export const deleteupvote_url = (post, user) => {
    return 'http://localhost:8000/api/posts/' + post.id + '/upvotes/' + user + '/'
};
export const fetchcreatedownvote_url = post => {
    return 'http://localhost:8000/api/posts/' + post.id + '/downvotes/'
};
export const deletedownvote_url = (post, user) => {
    return 'http://localhost:8000/api/posts/' + post.id + '/downvotes/' + user + '/'
};
