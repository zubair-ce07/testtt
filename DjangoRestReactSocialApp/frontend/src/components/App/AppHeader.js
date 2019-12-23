import React from 'react'
import * as auth from '../../helpers/auth'
import { Link } from 'react-router-dom'
import PropTypes from 'prop-types'

export const AppHeader = props => {
  const logout = () => {
    auth.logout()
    props.history.push('/login')
  }

  return (
    <nav className="navbar navbar-light bg-white">

      <Link className="navbar-brand" to="/home"> <img src="/ms-icon-150x150.png" alt="" width="60"/> Home</Link>

      <Link onClick={ () => logout()} to="/">Logout</Link>
    </nav>
  )
}

AppHeader.propTypes = {
  history: PropTypes.any
}
export default AppHeader
