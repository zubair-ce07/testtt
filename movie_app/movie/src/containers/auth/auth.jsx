import React from "react";
import { Redirect } from "react-router-dom";
import { FormField, Button } from "../../components";
import { Select, DatePicker } from "./components";
import { GENDER } from "../../utils/constants";
import "./auth.css";

class Auth extends React.Component {
  register = event => {
    event.preventDefault();
    this.props.loginForm();
  };

  handleChange = event => {
    let { user } = this.props;
    user[event.target.name] = event.target.value;
    this.props.updateUser(user);
  };

  handleSubmit = event => {
    event.preventDefault();
    this.props.isLoginForm
      ? this.props.loginUser(this.props.user)
      : this.props.registerUser(this.props.user);
  };

  render() {
    if (this.props.isAuthenticated) return <Redirect to="/" />;
    return (
      <div className="container">
        <div className="row">
          <div className="col-sm-4 auth">
            <form onSubmit={this.handleSubmit}>
              {this.props.error && (
                <div className="alert alert-danger" role="alert">
                  {this.props.error}
                </div>
              )}
              <FormField
                field="Email"
                type="email"
                icon="fa-envelope-o"
                name="email"
                onChange={this.handleChange}
                required
              />
              <FormField
                field="Password"
                type="password"
                icon="fa-key"
                name="password"
                onChange={this.handleChange}
                required
              />
              {!this.props.isLoginForm && (
                <React.Fragment>
                  <FormField
                    field="Confirm Password"
                    type="password"
                    icon="fa-key"
                    name="confirm_password"
                    onChange={this.handleChange}
                    required
                  />
                  <FormField
                    field="First Name"
                    type="text"
                    icon="fa-user-o"
                    name="first_name"
                    onChange={this.handleChange}
                    required
                  />
                  <FormField
                    field="Last Name"
                    type="text"
                    icon="fa-user-o"
                    name="last_name"
                    onChange={this.handleChange}
                    required
                  />
                  <Select
                    items={GENDER}
                    name="gender"
                    field="Gender"
                    onChange={this.handleChange}
                    required
                  />
                  <DatePicker
                    name="date_of_birth"
                    onChange={this.handleChange}
                    required
                  />
                </React.Fragment>
              )}

              <Button
                text={this.props.isLoginForm ? "Login" : "Register"}
                type="btn-primary btn-block"
              />
              <Button
                text={
                  this.props.isLoginForm
                    ? "Not have an account? Register here!"
                    : "Already have an account? Login!"
                }
                type="btn-link btn-block"
                onClick={this.register}
              />
            </form>
          </div>
        </div>
      </div>
    );
  }
}

export { Auth };
