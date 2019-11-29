import { Form, Formik } from "formik"
import React, { Component } from "react"

import { CustomField } from "./CustomFormikFields"
import { connect } from "react-redux"
import { signIn } from "../actions/authAction"

class LoginForm extends Component {
  constructor(props) {
    super(props)
    this.state = {
      initialValues: {
        username: "",
        password: ""
      }
    }
  }

  handleSubmit = (values, { setSubmitting }) => {
    this.props.onLogin(values)
    setSubmitting(false)
  }

  validate = values => {
    const errors = {}

    if (!values.username) {
      errors.username = "Username is required"
    }
    if (!values.password) {
      errors.password = "Password is required"
    }
    return errors
  }
  render() {
    const { initialValues } = this.state
    return (
      <div className="container mt-5">
        <div id="signin-form" className="card mx-auto bg-light border-dark p-5">
          <h1>Log In</h1>
          <Formik
            initialValues={initialValues}
            validate={this.validate}
            onSubmit={this.handleSubmit}
          >
            {props => (
              <div className="card-body bg-light">
                <Form>
                  <CustomField
                    label="User Name"
                    name="username"
                    placeholder="Username"
                  />
                  <CustomField
                    label="Password"
                    name="password"
                    placeholder="Password"
                    type="password"
                  />
                  <button
                    type="submit"
                    className="btn btn-primary"
                    disabled={props.isSubmitting}
                  >
                    Submit
                  </button>
                </Form>
              </div>
            )}
          </Formik>
        </div>
      </div>
    )
  }
}

const mapDispatchToProps = dispatch => {
  return {
    onLogin: formData => dispatch(signIn(formData))
  }
}

export default connect(null, mapDispatchToProps)(LoginForm)
