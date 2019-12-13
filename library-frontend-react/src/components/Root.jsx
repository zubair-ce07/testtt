import NavBar from "components/Navbar"
import PropTypes from "prop-types"
import { Provider } from "react-redux"
import React from "react"
import { Router } from "react-router-dom"
import Routes from "routes"
import history from "@history"

const Root = ({ store }) => {
  return (
    <Provider store={store}>
      <Router history={history}>
        <NavBar />
        <Routes />
      </Router>
    </Provider>
  )
}

Root.propTypes = {
  store: PropTypes.object.isRequired
}

export default Root
