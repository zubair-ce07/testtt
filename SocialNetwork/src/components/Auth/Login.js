import React from 'react';
import '../StyleSheets/Login.css'
import { login, signup } from '../../actions/auth'
import { connect } from 'react-redux';
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
        <input 
          type="text" 
          className="form-control" 
          placeholder="Enter Username"
          ref={(input) => { username_in = input; }}
        />
        <br/>
        <label>Password</label>
        <input 
          type="password" 
          className="form-control" 
          placeholder="Enter Password" 
          ref={(input) => { password_in = input; }}
        />
        <br/>
        <LinkContainer to="/">
          <button 
            className="btn btn-primary btn-block" 
            onClick={() => onSubmit(username_in.value,password_in.value)}
          >
            Log In
          </button>
        </LinkContainer>
      </div>
      <div className="form-group signupform well">
        <h5>Don't have an account?</h5>
        <label>Username</label>
        <input 
          type="text" 
          className="form-control" 
          placeholder="Enter Username" 
          ref={(input) => { username_up = input; }}
        />
        <br/>
        <label>Email</label>
        <input 
          type="email" 
          className="form-control" 
          placeholder="Enter Email" 
          ref={(input) => { email = input; }}
        />
        <br/>
        <label>Password</label>
        <input 
          type="password" 
          className="form-control" 
          placeholder="Enter Password" 
          ref={(input) => { password_up = input; }}
        />
        <br/>
        <LinkContainer to="/">
          <button 
            className="btn btn-primary btn-block" 
            onClick={() => onSignUp(username_up.value,email.value,password_up.value)}
          >
            Sign Up
          </button>
        </LinkContainer>
      </div>
    </div>
  );
}

const mapDispatchToProps = (dispatch) => ({
  onSubmit: (username,password) => {
    dispatch(login(username, password))
  },
  onSignUp: (username, email, password) => {
    dispatch(signup(username,email,password))
  }
})

const LoginHandler = connect(
  null,
  mapDispatchToProps
)(LoginForm)

export default LoginHandler;