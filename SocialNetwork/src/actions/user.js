import axios from 'axios'
import { LIST_USERS, FRIEND_ADDED} from './actions'

export const listUsers = (users) => ({
	type: LIST_USERS,
	users,
});

export const friendAdded = (friend) => ({
	type: FRIEND_ADDED,
	friend
});

export const fetchUsers = (token) => (
  function(dispatch){
  	axios({
      method: 'get',
      url: 'http://localhost:8000/testapp/userlist',
      headers: {
      Authorization: 'Token ' + token,
      },
    })
    .then(response => {
      dispatch(listUsers(response.data))
    })
    .catch(function(error){
      alert("Something Went Wrong")
    })
	}
)