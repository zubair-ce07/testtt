import React from 'react';
import {connect} from 'react-redux'
import {addLikeApi} from '../../actions/like'

const AddLike = ({postId, isLiked, token, addLikeHandler}) => (
	(isLiked === true)
		? <button 
				className="btn btn-default" 
				disabled>
				&#9989;
				<span>
					Liked
				</span>
		  </button>
		
		: <button 
				className="btn btn-primary" 
				onClick={() => addLikeHandler(postId, token)}>
				Like Post
		  </button>
)

const mapStateToProps = (state) => ({
	token: state.authReducer.token
})

const mapDispatchToProps = (dispatch) => ({
	addLikeHandler: (postId, token) => {
		dispatch(addLikeApi(postId, token))
	}
})

export default connect(
	mapStateToProps,
	mapDispatchToProps
)(AddLike)