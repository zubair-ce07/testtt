import React from 'react';
import {connect} from 'react-redux'
import axios from 'axios'
import {addComment} from '../../actions/comment'

const AddComment = ({postId, token, addCommentHandler}) => {
	let comment;
	console.log(postId)
	console.log(token)
	console.log(addCommentHandler)
	return (
		<div>
			<input type="text" className="form-control" placeholder="Add comment here..." ref={ input => { comment = input}} /><br/>
			<button className="btn btn-primary" onClick={() => addCommentHandler(comment, postId, token)} >Add Comment </button>
		</div>
	);
}

const mapStateToProps = (state) => {
	return {
		token: state.authReducer.token
	};
}

const mapDispatchToProps = (dispatch) => {
	return {
		addCommentHandler: (comment, postId, token) => {
			let data = new FormData()
			data.set('comment', comment.value)
			axios({
                method: 'post',
                url: 'http://localhost:8000/testapp/comment/'+postId+'/',
                headers: {
                Authorization: 'Token '+ token,
                },
                data: data
	        })
	        .then(response => {
	            dispatch(addComment(response.data))

	        })
	        .catch(function(error){
	            console.log(error)
	        })
	        
	        comment.value = ''
		}
	};
}

export default connect(
	mapStateToProps,
	mapDispatchToProps
)(AddComment)