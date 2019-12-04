import React from 'react'
import { Link } from 'react-router-dom'
import PropTypes from 'prop-types'
import { useDispatch } from 'react-redux'
import { Formik, Form, Field } from 'formik'
import * as Yup from 'yup'

import * as auth from '../helpers/auth'
import { login } from 'store/modules/user/user.action'
import { image } from '../helpers/assetHelper'
import { msgAlert } from '../helpers/common'
import AuthLayout from 'layouts/AuthLayout'

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
          onSubmit={values => {
            dispatch(login(values)).then((res) => {
              if (res.value.data.token) {
                auth.login(res.value.data)
                msgAlert('success', 'Logged In Successfully')
                props.history.push('/home')
              } else {
                msgAlert('failure', res.value.data.message)
              }
            })
          }}
        >
          {({ errors, touched }) => (
            <Form>
              <div className="form-group">
                <label htmlFor="your_name"><i className="zmdi zmdi-account material-icons-name"></i></label>
                <Field type="text" name="username" placeholder="Username"/>
                {errors.username && touched.username ? (<div>{errors.username}</div>) : null}
              </div>
              <div className="form-group">
                <label htmlFor="your_pass"><i className="zmdi zmdi-lock"></i></label>
                <Field type="password" name="password" placeholder="Password"/>
                {errors.password && touched.password ? (<div>{errors.password}</div>) : null}
              </div>
              {/* <div className="form-group">
            <input type="checkbox" name="remember-me" id="remember-me" className="agree-term" />
            <label htmlFor="remember-me" className="label-agree-term"><span><span></span></span>Remember me</label>
          </div> */}
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
