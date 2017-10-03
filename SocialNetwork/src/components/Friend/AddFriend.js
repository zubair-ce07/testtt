import React from 'react'
import {connect} from 'react-redux'
import {addFriendApi} from '../../actions/friend'

const AddFriend = ({userId, isFriend , addFriend, token, addFriendProfile}) => (
	(isFriend === true)
		? <button 
				className="btn btn-default" 
				disabled
		  >
		    &#9989;
		    <span>
		    	Friends
		    </span>
		  </button>

		: <button 
				className="btn btn-primary" 
				onClick={() => addFriend(userId, token, addFriendProfile)}>
				Add Friend
		  </button>
)

const mapStateToProps = (state) => ({
	token: state.authReducer.token,
})

const mapDispatchToProps = (dispatch) => ({
	addFriend: (id, token, addFriendProfile) => {
		dispatch(addFriendApi(id, token, addFriendProfile))
	}
})

export default connect(
	mapStateToProps,
	mapDispatchToProps
)(AddFriend)