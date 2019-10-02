import React from "react";
import { Redirect } from "react-router-dom";
import { Input, Button, Select, DatePicker } from "../../components";
import { GENDER } from "../../utils/constants";

class Auth extends React.Component {
  state = {
    isLoginForm: true
  }

  register = event => {
    event.preventDefault();
    this.setState({
      isLoginForm: !this.state.isLoginForm
    });
  };

  handleChange = event => {
    const { form } = this.props;
    this.props.updateForm({...form, [event.target.name]: event.target.value});
  };

  handleSubmit = event => {
    event.preventDefault();
    const {form} = this.props;
    if (!this.state.isLoginForm && form.password !== form.confirm_password) {
      this.props.authUserFailure("Passwords don't match");
      return;
    }
    this.state.isLoginForm
      ? this.props.loginUser(form)
      : this.props.registerUser(form);
  };

  render() {
    if (this.props.isAuthenticated) return <Redirect to="/" />;
    return (
      <div className="container">
        <div className="row">
          <div className="col-sm-4 offset-sm-4">
            <form onSubmit={this.handleSubmit}>
              {this.props.error && (
                <div className="alert alert-danger" role="alert">
                  {this.props.error}
                </div>
              )}
              <Input
                field="Email"
                type="email"
                icon="fa-envelope-o"
                name="email"
                onChange={this.handleChange}
                required
              />
              <Input
                field="Password"
                type="password"
                icon="fa-key"
                name="password"
                onChange={this.handleChange}
                required
              />
              {!this.state.isLoginForm && (
                <React.Fragment>
                  <Input
                    field="Confirm Password"
                    type="password"
                    icon="fa-key"
                    name="confirm_password"
                    onChange={this.handleChange}
                    required
                  />
                  <Input
                    field="First Name"
                    type="text"
                    icon="fa-user-o"
                    name="first_name"
                    onChange={this.handleChange}
                    required
                  />
                  <Input
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
                text={this.state.isLoginForm ? "Login" : "Register"}
                className="btn-primary btn-block"
                type="submit"
              />
              <Button
                text={
                  this.state.isLoginForm
                    ? "Not have an account? Register here!"
                    : "Already have an account? Login!"
                }
                className="btn-link btn-block"
                onClick={this.register}
                type="button"
              />
            </form>
          </div>
        </div>
      </div>
    );
  }
}

export { Auth };
