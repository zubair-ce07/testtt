import React from 'react'
import {connect} from 'react-redux'
import axios from 'axios'
import {friendAdded} from '../../actions/user'
import {updateFriends} from '../../actions/friend'

const AddFriend = ({userId, isFriend , addFriend, token, addFriendProfile}) => {

	if(isFriend === true){
		return <button className="btn btn-default" disabled>&#9989;<span>Friends</span></button>
	}
	else{
		return <button className="btn btn-primary" onClick={() => addFriend(userId, token, addFriendProfile)}>Add Friend</button>
	}
}

const mapStateToProps = (state) => {
	return {
		token: state.authReducer.token,
	};
}

const mapDispatchToProps = (dispatch) => {
	return {
		addFriend: (id, token, addFriendProfile) => {
			axios({
				method: 'post',
                url: 'http://localhost:8000/testapp/user/friend/'+id,
                headers: {
                Authorization: 'Token ' + token,
                },
			})
			.then(response => {
				dispatch(friendAdded(response.data.user))
				dispatch(updateFriends(response.data))
				if(addFriendProfile !== undefined){
					addFriendProfile()
				}
			})
			.then(function(err) {
				console.log(err)
			})
		},
	}
}

export default connect(
	mapStateToProps,
	mapDispatchToProps
)(AddFriend)