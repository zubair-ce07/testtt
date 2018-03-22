import React, { Component } from 'react';
import { connect } from 'react-redux';
import {loadPost, deleteComment, loadCategory, addComment, editComment} from "../actions/category";
import {editCommentSuccess} from '../actions/index'
import { bindActionCreators } from 'redux'
import FieldLevelValidationForm from '../containers/mainForm'
import _ from 'underscore'

import Timestamp from 'react-timestamp';import {
    BrowserRouter as Router,
    Link,
    Route // for later
} from 'react-router-dom'
class Post extends Component {
    constructor(props) {
        super(props);
        this.deleteComment = this.deleteComment.bind(this);
        this.editComment = this.editComment.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);

    }
    deleteComment(commentId) {

       this.props.dispatch(deleteComment(commentId));
    }
    editComment(commentId) {

       this.props.dispatch(editCommentSuccess(_.find(this.props.comments,{id:commentId})));
    }
    handleSubmit(formFields) {
        console.log(formFields)
        console.log(Math.random().toString(36).slice(2))
        this.props.dispatch(addComment({
            id:Math.random().toString(36).slice(2),
            parentId:this.props.post.id,
            author:formFields.author,
            body:formFields.body,
            timestamp:Date.now()

        }))
    }
    componentDidMount() {
        console.log(this.props)
        alert(this.props.match.params.post)
        this.props.dispatch(loadPost(this.props.match.params.post));

    }

    render(){
        const post= this.props.post;
        const comments= this.props.comments;
        return (

            <div className='container'>
                <h1>{post.title}</h1>

                <ul>
                    <li >{post.body}</li>
                    <li >{post.author}</li>
                    <li ><Timestamp time={post.timestamp} /></li>
                    <li >{post.voteScore}</li>

                </ul>
                <hr />
                <h2>Comments</h2>
                <ul>
                    {comments.map((comment)=>{
                        return <li key={comment.id} >
                            <button id='search-button' name='search-button' onClick={()=> {this.deleteComment(comment.id)}}> Delete</button>
                            <button id='search-button' name='search-button' onClick={()=> {this.editComment(comment.id)}}> Edit</button>
                            {comment.body}
                            </li>
                    })}

                </ul>
<FieldLevelValidationForm  onSubmit={this.handleSubmit}/>


            </div>

        )
    }
}
function mapStateToProps(state){
    console.log(state)
    return {
        allPosts: state.rootReducer.data.allPosts,
        posts: state.rootReducer.data.posts,
        categories: state.rootReducer.data.categories,
        post:state.rootReducer.data.post,
        comments:state.rootReducer.data.comments
    };
}

export default connect(mapStateToProps)(Post);