import React from 'react'
import { useDispatch } from 'react-redux'
import PropTypes from 'prop-types'

import { Route, Redirect } from 'react-router-dom'
import { getCurrentUser } from 'store/modules/user/user.action'

import { isLogin } from '../helpers/auth'

const ProtectedRoute = ({
  component: Component,
  ...rest
}) => {
  const dispatch = useDispatch()
  if (isLogin()) {
    dispatch(getCurrentUser())
  }

  return (
    <Route
      {...rest}
      render={props => {
        if (isLogin()) {
          return <Component {...props} />
        } else {
          return (
            <Redirect
              to={{
                pathname: '/login',
                state: {
                  from: props.location
                }
              }}
            />
          )
        }
      }}
    />
  )
}

ProtectedRoute.propTypes = {
  component: PropTypes.any,
  location: PropTypes.any
}

export default ProtectedRoute
