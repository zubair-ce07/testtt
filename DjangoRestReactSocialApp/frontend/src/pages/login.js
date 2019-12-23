import React from 'react'
import { Link } from 'react-router-dom'
import PropTypes from 'prop-types'
import { useDispatch } from 'react-redux'
import { Formik, Form, Field } from 'formik'
import * as Yup from 'yup'

import * as auth from '../helpers/auth'
import { login } from 'store/modules/user/user.action'
import { image } from '../helpers/assetHelper'
import { msgAlert, _exists } from '../helpers/common'
import AuthLayout from 'layouts/AuthLayout'
import TextField from 'components/UI/TextField'

const LoginSchema = Yup.object().shape({
  username: Yup.string()
    .min(2, 'Too Short!')
    .max(50, 'Too Long!')
    .required('Required'),
  password: Yup.string()
    .min(2, 'Too Short!')
    .max(50, 'Too Long!')
    .required('Required')
})

export const LoginPage = props => {
  const dispatch = useDispatch()
  return (
    <>
      <div className="signin-image">
        <figure><img src={image('signin-image.jpg')} alt=""/></figure>
        <Link className="signup-image-link" to="/register">Create an account</Link>

      </div>

      <div className="signin-form">
        <h2 className="form-title">Sign in</h2>
        <Formik
          initialValues={{ username: '', password: '' }}
          validationSchema={LoginSchema}
          onSubmit={(values, { setErrors }) => {
            dispatch(login(values)).then((res) => {
              if (_exists(res, 'value.data.token')) {
                auth.login(res.value.data)
                msgAlert('success', 'Logged In Successfully')
                props.history.push('/home')
              }
            }).catch((res) => {
              console.log(setErrors(res.data.message))
            })
          }}
        >
          {() => (
            <Form>

              <div className="form-group">
                <Field component={TextField} name="username" placeholder="Username" label="Username"/>
              </div>
              <div className="form-group">
                <Field type='password' component={TextField} name="password" placeholder="password" label="Password"/>
              </div>
              <div className="form-group form-button">
                <input type="submit" name="signin" id="signin" className="form-submit" value="Log in"/>
              </div>
            </Form>
          )}
        </Formik>
      </div>

    </>
  )
}

LoginPage.propTypes = {
  history: PropTypes.any
}
export default AuthLayout(LoginPage)
