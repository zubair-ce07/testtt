import React from "react";

import "./Login.css";

import djangoapi from "./djangoapi";

class Login extends React.Component {
  constructor(props) {
    super();
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleSubmit(e) {
    e.preventDefault();

    var username = this.refs.username.value;
    var pass = this.refs.password.value;

    djangoapi.login(username, pass, jsonData => {
      localStorage.username = username;
      localStorage.token = jsonData.token;
      window.location.reload();
    });
  }

  render() {
    return (
      <div className="absoluteContainer">
        <form id="loginForm" onSubmit={this.handleSubmit}>
          <input type="text" placeholder="username" ref="username" />
          <input type="password" placeholder="password" ref="password" />
          <input type="submit" />
        </form>
      </div>
    );
  }
}

export default Login;
