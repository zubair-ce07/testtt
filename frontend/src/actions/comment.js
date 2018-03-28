
import commentApi from '../api/comment';
import {deleteCommentSuccess,deleteCommentFailed, addCommentSuccess,
    addCommentFailed, updateCommentSuccess, updateCommentFailed} from './index';


export function deleteComment(commentId) {

    return function(dispatch) {

        commentApi.deleteComment(commentId).then(comment => {
            console.log(comment)
            dispatch(deleteCommentSuccess(comment, commentId));

        }).catch(error => {

            dispatch(deleteCommentFailed(error));
        });
    }
}
export function addComment(comment) {
    comment.timestamp=Date.now()
    return function(dispatch) {

        commentApi.addComment(comment).then(response => {
            console.log(response)
            dispatch(addCommentSuccess(response));

        }).catch(error => {

            dispatch(addCommentFailed(error));
        });
    }
}
export function updateComment(comment) {

    return function(dispatch) {

        commentApi.updateComment(comment,comment.id).then(response => {
            console.log(response)
            dispatch(updateCommentSuccess(response, comment.id));

        }).catch(error => {

            dispatch(updateCommentFailed(error));
        });
    }
}

