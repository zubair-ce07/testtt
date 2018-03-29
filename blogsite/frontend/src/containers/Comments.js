import React, { Component } from 'react';
import { connect } from 'react-redux';
import {deleteComment,addComment, updateComment} from '../actions/comment';
import {editCommentSuccess, createCommentSuccess} from '../actions/index'
import CommentForm from '../forms/CommentForm'
import ListHeader from '../containers/ListHeader'
import ListResource from './ListResource'

class Comments extends Component {
    constructor(props) {
        super(props);
        this.handleCreateSubmit = this.handleCreateSubmit.bind(this);
        this.handleEditSubmit = this.handleEditSubmit.bind(this);

    }

    handleCreateSubmit(comment) {
        this.props.addComment(comment)
    }
    handleEditSubmit(comment) {
        this.props.updateComment(comment)
    }

    render(){
        const comments= this.props.comments;
        const postId= this.props.post.id;
        return (

            <div className='container'>

                <h2>Comments</h2>
                <i  className={'glyphicon glyphicon-plus'}  onClick={()=> {this.props.createCommentSuccess(postId)}}> </i>

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

                {    this.props.editComment &&
                <CommentForm mode={'edit'}  onSubmit={this.handleEditSubmit}/>

                }
                {
                    this.props.createComment &&
                    <CommentForm  mode={'create'}  onSubmit={this.handleCreateSubmit}/>
                }

            </div>

        )
    }
}
function mapStateToProps(state){
    return {
        comments:state.rootReducer.posts.comments,
        createComment:state.rootReducer.posts.createComment,
        editComment:state.rootReducer.posts.editComment,
        post:state.rootReducer.posts.post,
    };
}
const mapDispatchToProps = (dispatch) => {
    return {
        deleteComment: (commentId) => {
            dispatch(deleteComment(commentId))
        },
        addComment: (comment) => {
            dispatch(addComment(comment))
        },
        updateComment:(comment) => {
            dispatch(updateComment(comment))
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