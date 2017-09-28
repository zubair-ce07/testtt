import React, {Component} from 'react'
import {connect} from 'react-redux'
import AddFriend from '../Friend/AddFriend'
import axios from 'axios'
import '../StyleSheets/PostList.css'
import {listUsers} from '../../actions/user'
import { LinkContainer } from 'react-router-bootstrap'


class UserList extends Component{
	componentDidMount(){
		axios({
                method: 'get',
                url: 'http://localhost:8000/testapp/userlist',
                headers: {
                Authorization: 'Token ' + this.props.token,
                },
	        })
	        .then(response => {
	            this.props.listUsersOnload(response.data)
	        })
	        .catch(function(error){
	            console.log(error)
	        })
	}

	render(){
		let users = this.props.users;
		return (
			<div className="postwell">
			{
				users.map(user => {
					return(
						<div key={user.id} style={{textAlign: "center"}}>
							<div className="row">
								<div className="col-sm-6"><LinkContainer to={"/profile/"+user.id}><a>{user.username}</a></LinkContainer></div>
								<AddFriend  isFriend={user.is_friend} userId={user.id} />
							</div><br />
						</div>

					);
				})
			}
			</div>
		);
	}
}

const mapStateToProps = (state) => {
	return {
		token: state.authReducer.token,
		users: state.userReducer.users,
	};
}

const mapDispatchToProps = (dispatch) => {
	return {
		listUsersOnload: (users) => {
			dispatch(listUsers(users))
		}
	};
}

export default connect(
	mapStateToProps,
	mapDispatchToProps
)(UserList)