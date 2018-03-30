import React, { Component } from 'react';
import { connect } from 'react-redux';
import {deleteComment} from '../actions/comment';
import {editCommentSuccess, createCommentSuccess} from '../actions/index'
import CommentForm from '../forms/CommentForm'
import ListHeader from '../containers/ListHeader'
import ListResource from './ListResource'

class Comments extends Component {
    render(){
        const comments= this.props.comments;
        const postId= this.props.post.id;
        return (

            <div className='container'>

                <h2>Comments</h2>
                <i  className='glyphicon glyphicon-plus'  onClick={()=> {this.props.createCommentSuccess(postId)}}> </i>

                {   comments.length>0 &&
                <ListHeader mode={'comments'}/>
                }
                <ListResource
                    resource={comments}
                    mode={'comments'}
                    onEditClick={(comment) =>
                        this.props.editCommentSuccess(comment)
                    }
                    onDeleteClick={(commentId) =>
                        (this.props.deleteComment(commentId))
                    }
                />

                {  this.props.commentFormType!=='' &&
                <CommentForm/>

                }

            </div>

        )
    }
}
function mapStateToProps(state){
    return {
        comments:state.rootReducer.posts.comments,
        post:state.rootReducer.posts.post,
        commentFormType:state.rootReducer.posts.commentFormType,
    };
}
const mapDispatchToProps = (dispatch) => {
    return {
        deleteComment: (commentId) => {
            dispatch(deleteComment(commentId))
        },
        editCommentSuccess:(comment) => {
            dispatch(editCommentSuccess(comment))
        },
        createCommentSuccess:(id) => {
            dispatch(createCommentSuccess(id))
        },

    }
}
export default connect(mapStateToProps,mapDispatchToProps)(Comments);