import React, { Component } from "react";

import {LoginForm} from './Form'

import {api} from "../.././utils/api";

export class Login extends Component {
  state = {
    institutions: []
  };
  submitLoginForm = event => {
    event.preventDefault();
    const { target : { elements} } = event
    const data = {username : elements.username.value , password : elements.password.value }
    api.post(`login/`, data)
      .then(({data: {token}}) => {
        localStorage.setItem('token', JSON.stringify(token));
        this.props.history.push(`/home`);
      })
      .catch((error) => {
        console.log('error', error.message);
        // todo show toast
      });

  }
  render() {
    return (
     <LoginForm submitForm = {this.submitLoginForm}  />
    );
  }
}
