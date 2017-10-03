import axios from 'axios';
import { LOGIN, LOGOUT} from './actions'


export const loginSuccess = (username, token, id) => ({
  type: LOGIN,
  username,
  token,
  id
});
 
export const logout = () => ({
  type: LOGOUT
});

export const login = (username, password) => (
  function(dispatch){    
    let data = new FormData()
    data.set('username',username)
    data.set('password', password)
    
    axios({
            method: 'post',
            url: 'http://localhost:8000/testapp/api-token-auth/',
            data: {
            username: username,
            password: password
        }
    })
    .then(function(response){
        dispatch(loginSuccess(username, response.data.token, response.data.id))  
    })
    .catch(function(error){
        alert("Unable to log in with provided credentials.")
        window.location.reload()
    })
  }
)

export const signup = (username, email, password) => (
  function(dispatch){
    let data = new FormData()
    data.set('username',username)
    data.set('password', password)
    data.set('email', email)

    axios({
            method: 'post',
            url: 'http://localhost:8000/testapp/user',
            data: data
    })
    .then(function(response){
        dispatch(loginSuccess(username, response.data.token, response.data.id))
    })
    .catch(function(error){
        alert("Unable to log in with provided credentials.")
    })
  }
)