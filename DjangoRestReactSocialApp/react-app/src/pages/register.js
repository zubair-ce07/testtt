import React from 'react'
import { image } from '../helpers/assetHelper'
import AuthLayout from 'layouts/AuthLayout'
import { Formik, Form, Field } from 'formik'
import { Link } from 'react-router-dom'
import * as Yup from 'yup'

const RegisterSchema = Yup.object().shape({
  first_name: Yup.string().min(2, 'Too Short!').max(50, 'Too Long!').required('Required'),
  last_name: Yup.string().min(2, 'Too Short!').max(50, 'Too Long!').required('Required'),
  username: Yup.string().min(2, 'Too Short!').max(50, 'Too Long!').required('Required'),
  password: Yup.string().min(2, 'Too Short!').max(50, 'Too Long!').required('Required'),
  re_password: Yup.string().oneOf([Yup.ref('password'), null], 'Passwords must match').required('Required')
})

export const LoginPage = props => {
  return (
    <>
      <div className="signin-form">
        <h2 className="form-title">Sign Up</h2>
        <Formik
          initialValues={{ username: '', first_name: '', last_name: '', password: '', re_password: '' }}
          validationSchema={RegisterSchema}
          onSubmit={values => {
            // same shape as initial values
            console.log(values)
          }}
        >
          {({ errors, touched }) => (
            <Form>
              <div className="form-group">
                <label htmlFor="your_name"><i className="zmdi zmdi-account material-icons-name"></i>First Name</label>
                <Field type="text" name="first_name" placeholder="First Name"/>
                {errors.first_name && touched.first_name ? (<div>{errors.first_name}</div>) : null}
              </div>
              <div className="form-group">
                <label htmlFor="your_name"><i className="zmdi zmdi-account material-icons-name"></i></label>
                <Field type="text" name="last_name" placeholder="Last Name"/>
                {errors.first_name && touched.last_name ? (<div>{errors.last_name}</div>) : null}
              </div>
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

              <div className="form-group">
                <label htmlFor="your_pass"><i className="zmdi zmdi-lock"></i></label>
                <Field type="re_password" name="re_password" placeholder="Re-Password"/>
                {errors.re_password && touched.re_password ? (<div>{errors.re_password}</div>) : null}
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
        <Link className="signup-image-link" to="/register">Create an account</Link>
      </div>

    </>
  )
}
export default AuthLayout(LoginPage)
