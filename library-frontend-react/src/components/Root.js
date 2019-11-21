import React from "react"
import PropTypes from "prop-types"
import { BrowserRouter as Router } from "react-router-dom"
import { Provider } from "react-redux"
import history from "../history"
import Routes from "../routes"

const Root = ({ store }) => {
  return (
    <Provider store={store}>
      <Router history={history}>
        <Routes />
      </Router>
    </Provider>
  )
}

Root.propTypes = {
  store: PropTypes.object.isRequired
}

export default Root
