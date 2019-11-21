import React from "react"
import { Link } from "react-router-dom"

const NavBar = ({ user }) => {
  return (
    <nav className="navbar sticky-top navbar-expand-lg navbar-dark bg-secondary">
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
            Books
          </a>
        </div>
        <div className="collapse navbar-collapse" id="navbarNavDropdown">
          <ul className="nav navbar-nav">
            <h1 className="navbar-brand">Hi {user.username || "Dummy"}!</h1>
            <li className="nav-item active">
              <Link to="/">Home</Link>
            </li>
            <li className="nav-item">
              <Link to="/cart">Cart</Link>
            </li>
          </ul>
          <ul className="navbar-nav ml-auto">
            <li className="nav-item active">
              <Link to="/cart">Cart</Link>
            </li>
            <li className="nav-item">
              <Link to="/cart">Cart</Link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  )
}

export default NavBar
