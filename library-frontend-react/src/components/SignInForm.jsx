import React, { Component } from "react"
import { connect } from "react-redux"
import { Formik, Form, Field, ErrorMessage } from "formik"

import { authorSignup } from "../actions/authAction"

class SignInForm extends Component {
  constructor(props) {
    super(props)
    this.state = {
      initialValues: {
        first_name: "",
        username: "",
        password: "",
        password2: ""
      }
    }
  }
  handleSubmit = (values, { setSubmitting }) => {
    console.log("props: ", this.props)
    this.props.onSignup(values)
  }

  validate = values => {
    const errors = {}
    const password = values.password
    const password2 = values.password2
    const minPasswordLength = 4

    if (!values.username) {
      errors.username = "Username is required"
    }
    if (!values.first_name) {
      errors.first_name = "First name is required"
    }
    if (!password) {
      errors.password = "Password is required"
    }
    if (!password2) {
      errors.password2 = "Confirmation password is required"
    }
    if (password && password2) {
      if (password === password2) {
        if (password.length < minPasswordLength)
          errors.password = `Pasword must be atleast ${minPasswordLength} digits`
      } else errors.password2 = "Paswords must match"
    }
    return errors
  }

  render() {
    const { initialValues } = this.state
    return (
      <div className="container">
        <h1>Author Signup</h1>
        <Formik
          initialValues={initialValues}
          validate={this.validate}
          onSubmit={this.handleSubmit}
        >
          {({ isSubmitting }) => (
            <Form>
              <div className="form-group">
                <label htmlFor="username">User Name</label>
                <Field
                  name="username"
                  className="form-control"
                  placeholder="Username"
                />
                <ErrorMessage
                  component="p"
                  name="username"
                  className="text-danger"
                />
              </div>
              <div className="form-group">
                <label htmlFor="first_name">First Name</label>
                <Field
                  name="first_name"
                  className="form-control"
                  placeholder="First name"
                />
                <ErrorMessage
                  component="p"
                  name="first_name"
                  className="text-danger"
                />
              </div>
              <div className="form-group">
                <label htmlFor="password">Password</label>
                <Field
                  type="password"
                  name="password"
                  placeholder="Password"
                  className="form-control"
                />
                <ErrorMessage
                  component="p"
                  name="password"
                  className="text-danger"
                />
              </div>
              <div className="form-group">
                <label htmlFor="password2">Confirm Password</label>
                <Field
                  type="password"
                  name="password2"
                  placeholder="Confirm Password"
                  className="form-control"
                />
                <ErrorMessage
                  component="p"
                  name="password2"
                  className="text-danger"
                />
              </div>
              <button
                type="submit"
                className="btn btn-primary"
                disabled={isSubmitting}
              >
                Submit
              </button>
            </Form>
          )}
        </Formik>
      </div>
    )
  }
}

const mapDispatchToProps = dispatch => {
  return {
    onSignup: formData => {
      dispatch(authorSignup(formData))
    }
  }
}

export default connect(null, mapDispatchToProps)(SignInForm)
