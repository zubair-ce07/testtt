import React from 'react';
import {connect} from 'react-redux'
import {addCommentApi} from '../../actions/comment'

const AddComment = ({postId, token, addCommentHandler}) => {
	let comment;
	return (
		<div>
			<input 
				type="text" 
				className="form-control" 
				placeholder="Add comment here..." 
				ref={ input => { comment = input}} 
			/>
			<br/>
			<button 
				className="btn btn-primary" 
				onClick={() => addCommentHandler(comment, postId, token)}>
				Add Comment 
			</button>
		</div>
	);
}

const mapStateToProps = (state) => ({
	token: state.authReducer.token
})

const mapDispatchToProps = (dispatch) => ({
	addCommentHandler: (comment, postId, token) => {
		dispatch(addCommentApi(comment, postId, token))
    comment.value = ''
	}
})

export default connect(
	mapStateToProps,
	mapDispatchToProps
)(AddComment)