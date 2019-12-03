import { Form, Formik } from "formik"
import React, { Component } from "react"

import { CustomField } from "./CustomFormikFields"
import ErrorDetails from "./ErrorDetails"
import Loader from "./Loader"
import { connect } from "react-redux"
import { publisherSignup } from "../actions/authAction"

class PublisherSignupForm extends Component {
  constructor(props) {
    super(props)
    this.state = {
      initialValues: {
        company_name: "",
        username: "",
        password: "",
        password2: ""
      }
    }
  }

  handleSubmit = (values, { setSubmitting }) => {
    this.props.onSignup(values)
    setSubmitting(false)
  }

  validate = values => {
    const errors = {}
    const password = values.password
    const password2 = values.password2
    const minPasswordLength = 4

    if (!values.username) {
      errors.username = "Username is required"
    }
    if (!values.company_name) {
      errors.company_name = "First name is required"
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
    const { errors, loading } = this.props

    if (loading) return <Loader />
    return (
      <div className="container mt-5">
        <div id="signup-form" className="card mx-auto bg-light border-dark p-5">
          <h1>Publisher Signup</h1>
          <ErrorDetails errors={errors} />
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
                    label="Company Name"
                    name="company_name"
                    placeholder="Company Name"
                  />

                  <CustomField
                    label="Password (Must be atleast 4 digits)"
                    name="password"
                    placeholder="Password"
                    type="password"
                  />

                  <CustomField
                    label="Confirm Password"
                    name="password2"
                    placeholder="Confirm Password"
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

const mapStateToProps = (state, _ownProps) => {
  return {
    errors: state.auth.error,
    loading: state.auth.loading
  }
}

const mapDispatchToProps = dispatch => {
  return {
    onSignup: formData => {
      dispatch(publisherSignup(formData))
    }
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(PublisherSignupForm)
