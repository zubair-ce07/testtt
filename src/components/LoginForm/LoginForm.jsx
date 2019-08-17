import React, { Component } from "react";
import { Field, Form } from "react-final-form";
import { connect } from "react-redux";

import { loginUser } from "../../actions/user.action";
import history from "../../history";

import "./LoginForm.css";

class LoginForm extends Component {
  state = {};

  onSubmit = credentials => {
    this.props.loginUser(credentials);
  };

  renderStatus = () => {
    const { error } = this.props.auth;
    if (error) return <div>{error}</div>;
  };

  renderError = ({ error, touched }) => {
    if (error && touched) return <div>{error}</div>;
  };

  renderInput = ({ input, label, meta }) => {
    const inputClass = `form-control ${
      meta.error && meta.touched ? "is-invalid" : ""
    }`;
    return (
      <div className="form-group row">
        <label className="col-sm-2 col-form-label">{label}</label>
        <div className="col-sm-6">
          <input {...input} type={input.type} className={inputClass} />
          {this.renderError(meta)}
        </div>
      </div>
    );
  };

  register() {
    history.push("/register");
  }

  renderForm = ({ handleSubmit }) => {
    return (
      <>
        <form onSubmit={handleSubmit}>
          <Field
            name="email"
            type="text"
            label="Email"
            component={this.renderInput}
          />
          <Field
            name="password"
            type="password"
            label="Password"
            component={this.renderInput}
          />
          <button className="btn btn-primary">Login</button>
        </form>
        <button className="btn btn-primary" onClick={this.register}>
          Register
        </button>
      </>
    );
  };

  render = () => {
    return (
      <>
        <Form
          onSubmit={this.onSubmit}
          validate={validate}
          render={this.renderForm}
        />
        {this.renderStatus()}
      </>
    );
  };
}

const validate = formValues => {
  const errors = {};

  if (!formValues.email) errors.email = "Please enter your email";
  if (!formValues.password) errors.password = "Please enter you password";

  return errors;
};

const mapStateToProps = state => {
  return { auth: state.auth };
};

export default connect(
  mapStateToProps,
  { loginUser }
)(LoginForm);
