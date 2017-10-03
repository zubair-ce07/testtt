import axios from 'axios'
import { LIST_FRIENDS, UPDATE_FRIENDS} from './actions'
import {friendAdded} from './user'


export const listFriends = (friends) => ({
	type: LIST_FRIENDS,
	friends,
});

export const updateFriends = (friend) => ({
	type: UPDATE_FRIENDS,
	friend
});

export const addFriendApi = (id, token, addFriendProfile) => (
	function(dispatch){
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
		.catch(function(err) {
            alert("Something Went Wrong")
		})
	}
)

export const fetchUserFriendsApi = (token) => (
	function(dispatch){
		axios({
      method: 'get',
      url: 'http://localhost:8000/testapp/user/friends',
      headers: {
      Authorization: 'Token '+token,
      }
    })
    .then(response => {
        dispatch(listFriends(response.data))

    })
    .catch(function(error){
        alert("Something Went Wrong")
    })
	}
)