import React, { Component } from "react"

import { Link } from "react-router-dom"
import { connect } from "react-redux"
import { signOut } from "../actions/authAction"
import url from "../urls"

class NavBar extends Component {
  handlelogout = () => {
    this.setState({ user: {} })
    this.props.onLogout()
  }

  render() {
    const { user } = this.props
    const isLogedIn = Boolean(user && user.token)
    return (
      <nav
        id="lib-nav"
        className="navbar sticky-top navbar-expand-lg navbar-dark bg-secondary"
      >
        <div className="container-fluid">
          <button
            className="navbar-toggler"
            type="button"
            data-toggle="collapse"
            data-target="#navbarTogglerDemo01"
            aria-controls="navbarTogglerDemo01"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="navbar-header">
            <a className="navbar-brand" href="#/">
              My Library
            </a>
          </div>
          <div className="collapse navbar-collapse" id="navbarNavDropdown">
            {isLogedIn && (
              <ul className="nav navbar-nav">
                <li className="nav-item">
                  <Link to={url.books}>Books</Link>
                </li>
                <li className="nav-item">
                  <Link to={url.authors}>Authors</Link>
                </li>
                <li className="nav-item">
                  <Link to={url.publishers}>Publishers</Link>
                </li>
                <li className="nav-item">
                  <Link to={url.categories}>Categories</Link>
                </li>
              </ul>
            )}
            <ul className="navbar-nav ml-auto">
              {isLogedIn ? (
                <React.Fragment>
                  <li className="username nav-item">
                    Hi {user.name || user.username}!
                  </li>
                  <li className="nav-item">
                    <a className="logout" href="#" onClick={this.handlelogout}>
                      Logout
                    </a>
                  </li>
                </React.Fragment>
              ) : (
                <React.Fragment>
                  <li className="nav-item">
                    <Link to={url.authorSignUp}>Author SignUp</Link>
                  </li>
                  <li className="nav-item">
                    <Link to={url.publisherSignUp}>Publisher SignUp</Link>
                  </li>
                  <li className="nav-item">
                    <Link to={url.login}>LogIn</Link>
                  </li>
                </React.Fragment>
              )}
            </ul>
          </div>
        </div>
      </nav>
    )
  }
}

const mapStateToProps = (state, _ownProps) => {
  return {
    user: state.auth.currentUser,
    loading: state.auth.loading
  }
}

const mapDispatchToProps = dispatch => {
  return {
    onLogout: () => dispatch(signOut())
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(NavBar)
