import React from 'react'
import PropTypes from 'prop-types'
import { Route, Redirect } from 'react-router-dom'

import { isLogin } from '../helpers/auth'

const UserRoute = ({
  component: Component,
  ...rest
}) => {
  return (
    <Route
      {...rest}
      render={props => {
        if (!isLogin()) {
          return <Component {...props} />
        } else {
          return (
            <Redirect
              to={{
                pathname: '/home',
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

UserRoute.propTypes = {
  component: PropTypes.any,
  location: PropTypes.any
}

export default UserRoute
