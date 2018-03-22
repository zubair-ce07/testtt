
import CategoryApi from '../api/categoryApi';
import {loadCategorySuccess, loadCategoryFailed, loadCategoryRequest,
    getPostsSuccess ,getPostsFailed,getAllPostsSuccess ,
    getAllPostsFailed,getPostSuccess,getPostFailed,
    deleteCommentSuccess,deleteCommentFailed,
    addCommentSuccess, addCommentFailed, editCommentSuccess, editCommentFailed} from './index';

export function loadCategory() {
    return function(dispatch) {

        return CategoryApi.getCategoryData().then(categories => {

            dispatch(loadCategorySuccess(categories));

        }).catch(error => {

            dispatch(loadCategoryFailed(error));
        });
    }
}
export function loadPosts(category) {

    return function(dispatch) {

        CategoryApi.getPostsData(category).then(posts => {
console.log(posts)
            dispatch(getPostsSuccess(posts));

        }).catch(error => {

            dispatch(getPostsFailed(error));
        });
    }
}
export function loadAllPosts() {

    return function(dispatch) {

        CategoryApi.getAllPostsData().then(posts => {
console.log(posts)
            dispatch(getAllPostsSuccess(posts));

        }).catch(error => {

            dispatch(getAllPostsFailed(error));
        });
    }
}
export function loadPost(postId) {

    return function(dispatch) {

        CategoryApi.getPost(postId).then(post => {
            console.log(post)
            if(post.commentCount>0){
                CategoryApi.getComments(postId).then(comments =>{

                    dispatch(getPostSuccess(post, comments));


                })
                    .catch(error => {

                    })
            }

        }).catch(error => {

            dispatch(getPostFailed(error));
        });
    }
}
export function deleteComment(commentId) {

    return function(dispatch) {

        CategoryApi.deleteComment(commentId).then(comment => {
            console.log(comment)
            dispatch(deleteCommentSuccess(comment, commentId));

        }).catch(error => {

            dispatch(deleteCommentFailed(error));
        });
    }
}
export function addComment(comment) {

    return function(dispatch) {

        CategoryApi.addComment(comment).then(response => {
            console.log(response)
            dispatch(addCommentSuccess(response));

        }).catch(error => {

            dispatch(addCommentFailed(error));
        });
    }
}
export function editComment(commentId, comment) {

    return function(dispatch) {

        CategoryApi.editComment(commentId,comment).then(response => {
            console.log(response)
            dispatch(editCommentSuccess(response));

        }).catch(error => {

            dispatch(editCommentFailed(error));
        });
    }
}
