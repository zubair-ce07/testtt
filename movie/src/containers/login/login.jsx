import React from "react";
import { FormField, Button } from "../../components";
import "./login.css";

class LoginView extends React.Component {
  handleLogin = e => {
    e.preventDefault();
    const {email, password} = e.target;
    this.props.loginUser({
      email: email.value,
      password: password.value
    });
  };

  render() {
    return (
      <div className="login">
        <form onSubmit={this.handleLogin}>
          <FormField name="email" field="Email" type="text" icon="fa-user"  />
          <FormField name="password" field="Password" type="password" icon="fa-key" />
          <Button text="Login" />
          <a href="#">Create Account</a>
        </form>
      </div>
    );
  }
}

export { LoginView };
