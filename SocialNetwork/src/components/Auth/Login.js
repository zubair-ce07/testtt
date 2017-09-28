import React from 'react';
import '../StyleSheets/Login.css'
import { login } from '../../actions/auth'
import { connect } from 'react-redux';
import axios from 'axios';
import { saveState } from '../../localStorage'
import { LinkContainer } from 'react-router-bootstrap'



const LoginForm = ({onSubmit,onSignUp}) => {
        let username_in;
        let password_in;
        let username_up;
        let password_up;
        let email;
        return (
            <div>
                <div className="form-group signinform well" >
                    <label>Username</label>
                    <input type="text" className="form-control" placeholder="Enter Username" ref={(input) => { username_in = input; }}/>
                    <br/>
                    <label>Password</label>
                    <input type="password" className="form-control" placeholder="Enter Password" ref={(input) => { password_in = input; }}/>
                    <br/>
                    <LinkContainer to="/">
                        <button className="btn btn-primary btn-block" onClick={() => onSubmit(username_in.value,password_in.value)}>Log In</button>
                    </LinkContainer>
                </div>
                <div className="form-group signupform well">
                    <h5>Don't have an account? </h5>
                    <label>Username</label>
                    <input type="text" className="form-control" placeholder="Enter Username" ref={(input) => { username_up = input; }}/>
                    <br/>
                    <label>Email</label>
                    <input type="email" className="form-control" placeholder="Enter Email" ref={(input) => { email = input; }}/>
                    <br/>
                    <label>Password</label>
                    <input type="password" className="form-control" placeholder="Enter Password" ref={(input) => { password_up = input; }}/>
                    <br/>
                    <LinkContainer to="/">
                        <button className="btn btn-primary btn-block" onClick={() => onSignUp(username_up.value,email.value,password_up.value)}>Sign Up</button>
                    </LinkContainer>
                </div>
            </div>
        );
}

const mapDispatchToProps = (dispatch) => {
    return {
        onSubmit: (username,password) => {
        
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
                dispatch(login(username, response.data.token, response.data.id))
                let auth_state = {isLoggedIn: true, username: username, token: response.data.token, id: response.data.id}
                saveState(auth_state)
            })
            .catch(function(error){
                alert("Unable to log in with provided credentials.")
                window.location.reload()

            })
        },
        onSignUp: (username, email, password) => {

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
                console.log(response.data)
                dispatch(login(username, response.data.token, response.data.id))
                let auth_state = {isLoggedIn: true, username: username, token: response.data.token, id: response.data.id}
                saveState(auth_state)
            })
            .catch(function(error){
                alert("Unable to log in with provided credentials.")
            })
        }
    };
}

const LoginHandler = connect(
    undefined,
    mapDispatchToProps
    )(LoginForm)

export default LoginHandler;