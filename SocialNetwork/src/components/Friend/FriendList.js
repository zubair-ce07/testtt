import React, {Component} from 'react';
import { connect } from 'react-redux';
import { fetchUserFriendsApi } from '../../actions/friend'
import '../StyleSheets/PostList.css'


class FriendList extends Component{
	 
	componentDidMount(){
		/* getting user friends */
		this.props.fetchUserFriends(this.props.token)
  }

  render(){
  	const {friends} = this.props
		return (
			<div>
			{
				friends.map( friend => {
					return(
						<div className="postwell" key={friend.user.id}>
							<p>
								{friend.user.username}
							</p>
						</div>
					);
				})
			}
			</div>
		);
	}
}

const mapStateToProps = (state) => ({
  token: state.authReducer.token,
  friends: state.friendReducer.friends
})

const mapDispatchToProps = (dispatch) => ({
  fetchUserFriends: (token) => {
    dispatch(fetchUserFriendsApi(token))
  }
})

export default connect(
	mapStateToProps,
	mapDispatchToProps
)(FriendList);