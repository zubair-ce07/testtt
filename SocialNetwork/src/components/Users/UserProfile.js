import React, {Component} from 'react'
import {connect} from 'react-redux'
import AddFriend from '../Friend/AddFriend'
import axios from 'axios'

class UserProfile extends Component {
	constructor(props){
		super(props)

		this.state = {id: '', 'username': '', 'email': '' , is_friend: ''}
		this.addFriendClicked = this.addFriendClicked.bind(this)
	}
	componentDidMount(){
		axios({
	    method: 'get',
	    url: 'http://localhost:8000/testapp/user/'+this.props.match.params.id+'/',
	    headers: {
	    Authorization: 'Token ' + this.props.token,
		  },
    })
    .then(response => {
    	const {id , username, email, is_friend} = response.data
      this.setState({id: id , username: username, email: email, is_friend: is_friend})
    })
    .catch(function(error){
      console.log(error)
    })		
	}

	addFriendClicked(){
		let currState = this.state
		currState["is_friend"] = true 
		this.setState(currState)
	}

	render(){
		let is_user_himself;
		if(this.props.id !== this.state.id){
			is_user_himself = (
				<AddFriend  
					isFriend={this.state.is_friend} 
					userId={this.state.id} 
					addFriendProfile={this.addFriendClicked}
				/>
			);
		}
		if (this.state.id === ''){
			return <h1>User not found</h1>
		}
		else{
			return(
				<div className="well" style={{textAlign: "center"}}> 
					<h1>profile</h1>
					<p>{this.state.username}</p>
					<p>{this.state.email}</p>
					{is_user_himself}
				</div>
			);
		}
	}
}

const mapStateToProps =(state) => ({
	token: state.authReducer.token,
	id: state.authReducer.id
})


export default connect(mapStateToProps)(UserProfile);