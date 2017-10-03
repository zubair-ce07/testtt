import React, {Component} from 'react'
import {connect} from 'react-redux'
import AddFriend from '../Friend/AddFriend'
import '../StyleSheets/PostList.css'
import {fetchUsers} from '../../actions/user'
import { LinkContainer } from 'react-router-bootstrap'


class UserList extends Component{
	componentDidMount(){
		this.props.listUsersOnload(this.props.token)
	}

	render(){
		const users = this.props.users;
		return (
			<div className="postwell">
			{
				users.map(user => {
					return (
						<div key={user.id} style={{textAlign: "center"}}>
							<div className="row">
								<div className="col-sm-6">
									<LinkContainer to={"/profile/"+user.id}>
										<a>{user.username}</a>
									</LinkContainer>
								</div>
								<AddFriend 
									isFriend={user.is_friend} 
									userId={user.id}
								/>
							</div>
							<br />
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
	users: state.userReducer.users,
})

const mapDispatchToProps = (dispatch) => ({
	listUsersOnload: (token) => {
		dispatch(fetchUsers(token))
	},
})

export default connect(
	mapStateToProps,
	mapDispatchToProps
)(UserList)