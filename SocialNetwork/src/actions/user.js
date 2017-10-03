import axios from 'axios'

export const listUsers = (users) => ({
	type: "LIST_USERS",
	users,
});

export const friendAdded = (friend) => ({
	type: "FRIEND_ADDED",
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