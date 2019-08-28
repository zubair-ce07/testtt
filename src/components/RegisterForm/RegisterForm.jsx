import React, { Component } from "react";
import { Field, Form } from "react-final-form";
import { connect } from "react-redux";
import { registerUser } from "../../actions/auth.actions";

import "./Form.sass";
import history from "../../history";

class RegisterForm extends Component {
  state = {};

  onSubmit = formValues => {
    const newUser = { ...formValues };
    delete newUser.confirm;
    this.props.registerUser(newUser);
  };

  renderStatusErrors = message => {
    // Object.keys(message).map((key, i) => {
    //   return (
    //     <div key={i}>
    //       {message[key].map((m, j) => {
    //         return <div key={j}>{m}</div>;
    //       })}
    //     </div>
    //   );
    // });
    // let errors = "";
    // for (const key in message) {
    //   errors += key + ": ";
    //   message[key].forEach(m => (errors += m));
    // }
    // return errors;
    return JSON.stringify(message);
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
          {this.renderStatusErrors(message)}
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
          name="first_name"
          type="text"
          label="First Name"
          component={this.renderInput}
        />
        <Field
          name="last_name"
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

  if (!formValues.first_name)
    errors.first_name = "Please enter your first name";

  if (!formValues.last_name) errors.last_name = "Please enter your last name";

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
