import React, { Component } from 'react';
import { connect } from 'react-redux';
import {deleteComment,addComment, updateComment} from "../actions/comment";
import {editCommentSuccess, createCommentSuccess} from '../actions/index'
import CommentForm from '../forms/CommentForm'
import ListHeader from '../containers/ListHeader'
import ListResource from './ListResource'

class Comments extends Component {
    constructor(props) {
        super(props);
        this.handleCreateSubmit = this.handleCreateSubmit.bind(this);
        this.handleEditSubmit = this.handleEditSubmit.bind(this);
        this.handleEditSubmit = this.handleEditSubmit.bind(this);

    }

    handleCreateSubmit(comment) {
        console.log(comment);
        this.props.dispatch(addComment(comment))
    }
    handleEditSubmit(comment) {
        this.props.dispatch(updateComment(comment))
    }

    render(){
        const comments= this.props.comments;
        return (

            <div className='container'>

                <h2>Comments</h2>
                <i  className={'glyphicon glyphicon-plus'}  onClick={()=> {this.props.dispatch(createCommentSuccess())}}> </i>

                {   comments.length>0 &&
                <ListHeader resource={'comments'}/>
                }
                <ListResource
                    resource={comments}
                    path={''}
                    mode={'comments'}
                    onEditClick={(comment) =>
                        this.props.dispatch(editCommentSuccess(comment))
                    }
                    onDeleteClick={(commentId) =>
                        (this.props.dispatch(deleteComment(commentId)))
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
    console.log(state)
    return {
        comments:state.rootReducer.posts.comments,
        createComment:state.rootReducer.comments.createComment,
        editComment:state.rootReducer.comments.editComment,
    };
}

export default connect(mapStateToProps)(Comments);