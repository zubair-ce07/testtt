import React from 'react'
import { useDispatch } from 'react-redux'
import PropTypes from 'prop-types'
import { Link } from 'react-router-dom'
import { Formik, Form, Field } from 'formik'
import * as Yup from 'yup'

import AuthLayout from 'layouts/AuthLayout'
import { register } from 'store/modules/user/user.action'
import { msgAlert } from '../helpers/common'
import { image } from '../helpers/assetHelper'
import TextField from 'components/UI/TextField'

const RegisterSchema = Yup.object().shape({
  first_name: Yup.string().min(2, 'Too Short!').max(50, 'Too Long!').required('Required'),
  last_name: Yup.string().min(2, 'Too Short!').max(50, 'Too Long!').required('Required'),
  username: Yup.string().min(2, 'Too Short!').max(50, 'Too Long!').required('Required'),
  password: Yup.string().min(2, 'Too Short!').max(50, 'Too Long!').required('Required'),
  re_password: Yup.string().oneOf([Yup.ref('password'), null], 'Passwords must match').required('Required')
})

export const Register = props => {
  const dispatch = useDispatch()
  return (
    <>
      <div className="signin-form">
        <h2 className="form-title">Sign Up</h2>
        <Formik
          initialValues={{ username: '', first_name: '', last_name: '', password: '', re_password: '' }}
          validationSchema={RegisterSchema}
          onSubmit={(values, { setErrors }) => {
            dispatch(register(values)).then((res) => {
              if (res.value.data.status) {
                msgAlert('success', 'Registered Successfully')
                props.history.push('/login')
              } else {
                msgAlert('failure', res.value.data.message)
              }
            }).catch((res) => {
              setErrors(res.data.message)
            })
          }}
        >
          {() => (
            <Form>
              <div className="form-group">
                <Field component={TextField} name="first_name" placeholder="First Name" label="First Name"/>
              </div>
              <div className="form-group">
                <Field component={TextField} name="last_name" placeholder="Last Name" label="Last Name"/>
              </div>
              <div className="form-group">
                <Field component={TextField} name="username" placeholder="Username" label="Username"/>
              </div>

              <div className="form-group">
                <Field type="password" component={TextField} name="password" placeholder="Password" label="Password"/>
              </div>

              <div className="form-group">
                <Field type="password" component={TextField} name="re_password" placeholder="Re-Password" label="Re-Password"/>
              </div>
              <div className="form-group form-button">
                <input type="submit" name="signin" id="signin" className="form-submit" value="Register"/>
              </div>
            </Form>
          )}
        </Formik>
      </div>

      <div className="signin-image">
        <figure><img src={image('signup-image.jpg')} alt=""/></figure>
        <Link className="signup-image-link" to="/login">Already have an account</Link>
      </div>

    </>
  )
}

Register.propTypes = {
  history: PropTypes.any
}
export default AuthLayout(Register)
