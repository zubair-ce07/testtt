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
      <Link className="navbar-brand" to="/home">Social App</Link>
      <form className="form-inline">
        <div className="input-group">
          <input type="text" className="form-control" aria-label="Recipient's username" aria-describedby="button-addon2"/>
          <div className="input-group-append">
            <button className="btn btn-outline-primary" type="button" id="button-addon2">
              <i className="fa fa-search"></i>
            </button>
          </div>
        </div>
      </form>
      <Link onClick={ () => logout()} to="/">Logout</Link>
    </nav>
  )
}

AppHeader.propTypes = {
  history: PropTypes.any
}
export default AppHeader
