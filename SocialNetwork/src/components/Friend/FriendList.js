import React, {Component} from 'react';
import { connect } from 'react-redux';
import { listFriend } from '../../actions/friend'
import axios from 'axios'
import '../StyleSheets/PostList.css'


class FriendList extends Component{
	 
	 componentDidMount(){
        /* getting user friends */
        axios({
                method: 'get',
                url: 'http://localhost:8000/testapp/user/friends',
                headers: {
                Authorization: 'Token '+this.props.token,
                }
        })
        .then(response => {
            this.props.listFriends(response.data)

        })
        .catch(function(error){
            console.log(error)
        })

        

    }

    render(){
    	const {friends} = this.props
		return (
			<div>
				{
					friends.map( friend => {
						return(
						<div className="postwell" key={friend.user.id}>
							<p>{friend.user.username}</p>
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
        friends: state.friendReducer.friends
    };
}

const mapDispatchToProps = (dispatch) => {
    return {
        listFriends: (friends) => {
            dispatch(listFriend(friends))
        },
    }
}

export default connect(
	mapStateToProps,
	mapDispatchToProps
)(FriendList);