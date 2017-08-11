import React from "react";

import "./Login.css";

import djangoapi from "../djangoapi";

class Login extends React.Component {
  handleSubmit(e) {
    e.preventDefault();

    djangoapi.login(username, pass, jsonData => {
      localStorage.username = username;
      localStorage.token = jsonData.token;
    });
  }

  render() {
    return (
      <div className="absoluteContainer">
        <form id="loginForm" onSubmit={this.handleSubmit}>
          <input type="text" placeholder="username" name="username" />
          <input type="password" placeholder="password" name="password" />
          <input type="submit" />
        </form>
      </div>
    );
  }
}

export default Login;
