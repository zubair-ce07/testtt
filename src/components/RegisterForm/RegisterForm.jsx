import React, { Component } from "react";
import { Field, Form } from "react-final-form";
import { connect } from "react-redux";
import { registerUser } from "../../actions/user.actions";

import "./Form.sass";
import history from "../../history";

class RegisterForm extends Component {
  state = {};

  onSubmit = formValues => {
    const newUser = { ...formValues };
    delete newUser.confirm;
    this.props.registerUser(newUser);
  };

  renderStatus = () => {
    const { status, message } = this.props.registerStatus;
    if (status === "") return <div />;
    if (status === "Success")
      return (
        <>
          <div className="alert alert-success" role="alert">
            {message}
          </div>
          <div>Redirecting to login page</div>
        </>
      );
    if (status === "Failure")
      return (
        <div className="alert alert-warning" role="alert">
          {message}
        </div>
      );
  };

  renderError = ({ error, touched }) => {
    if (error && touched) return <div>{error}</div>;
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

  renderForm = ({ handleSubmit }) => {
    return (
      <form onSubmit={handleSubmit}>
        <Field
          name="firstName"
          type="text"
          label="First Name"
          component={this.renderInput}
        />
        <Field
          name="lastName"
          type="text"
          label="Last Name"
          component={this.renderInput}
        />
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
        <Field
          name="confirm"
          type="password"
          label="Confirm Password"
          component={this.renderInput}
        />
        <div className="buttons">
          <button className="btn btn-light">Register</button>
          <span onClick={this.login}>Already registered?</span>
        </div>
      </form>
    );
  };

  login = () => {
    history.push("/login");
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

  if (!formValues.firstName) errors.firstName = "Please enter your first name";

  if (!formValues.lastName) errors.lastName = "Please enter your last name";

  if (!formValues.email) errors.email = "Please enter you email";

  if (!formValues.password) errors.password = "Please enter your password";

  if (!formValues.confirm) errors.confirm = "Please confirm your password";

  if (formValues.password !== formValues.confirm)
    errors.confirm = "Passwords do no match";

  return errors;
};

const mapStateToProps = state => {
  return { registerStatus: state.registerStatus };
};

export default connect(
  mapStateToProps,
  { registerUser }
)(RegisterForm);
