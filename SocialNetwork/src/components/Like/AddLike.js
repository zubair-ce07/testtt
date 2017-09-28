import React from 'react';
import {connect} from 'react-redux'
import axios from 'axios'
import {addLike} from '../../actions/like'
import {postLiked} from '../../actions/post'

const AddLike = ({postId, isLiked, token, addLikeHandler}) => {
	if (isLiked === true){
		return <button className="btn btn-default" disabled>&#9989;<span>Liked</span></button>
	}
	else{ 
		return <button className="btn btn-primary" onClick={() => addLikeHandler(postId, token)}>Like Post</button>
	}
}

const mapStateToProps = (state) => {
	return {
		token: state.authReducer.token
	};
}

const mapDispatchToProps = (dispatch) => {
	return {
		addLikeHandler: (postId, token) => {
			axios({
                method: 'post',
                url: 'http://localhost:8000/testapp/like/'+postId+'/',
                headers: {
                Authorization: 'Token '+ token,
                },
	        })
	        .then(response => {
	            dispatch(addLike(response.data))
	            dispatch(postLiked(postId))

	        })
	        .catch(function(error){
	            console.log(error)
	        })
	        
		}
	};
}

export default connect(
	mapStateToProps,
	mapDispatchToProps
)(AddLike)