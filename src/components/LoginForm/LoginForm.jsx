import React, { Component } from "react";
import { Field, Form } from "react-final-form";
import { connect } from "react-redux";

import { loginUser } from "../../actions/auth.actions";
import history from "../../history";

import "../RegisterForm/Form.sass";

class LoginForm extends Component {
  state = {};

  onSubmit = credentials => {
    this.props.loginUser(credentials);
  };

  renderStatus = () => {
    const { error } = this.props.auth;
    if (error) return <div className="error">{error}</div>;
  };

  renderError = ({ error, touched }) => {
    if (error && touched) return <div className="error">{error}</div>;
  };

  renderInput = ({ input, label, meta }) => {
    const inputClass = `form-control ${
      meta.error && meta.touched ? "is-invalid" : ""
    }`;
    return (
      <div className="">
        <label className="">{label}</label>
        <div className="">
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
          <div className="buttons">
            <button className="btn btn-light">Login</button>
            <span onClick={this.register}>Not registered?</span>
          </div>
        </form>
      </>
    );
  };

  render = () => {
    return (
      <div className="Form">
        <div className="card">
          <Form
            onSubmit={this.onSubmit}
            validate={validate}
            render={this.renderForm}
          />
          {this.renderStatus()}
        </div>
      </div>
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
