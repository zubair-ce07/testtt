import React from "react"
import { Switch, Route, Redirect } from "react-router-dom"
import Cookies from "js-cookie"

import urls from "./urls"
import App from "./components/App"
import AuthorSignUpForm from "./components/AuthorSignUpForm"
import BooksList from "./components/BooksList"

const isUserAuthenticated = () => {
  return Boolean(Cookies.get("Authorization"))
}

const PrivateRoute = ({ children, ...rest }) => {
  console.log("is authenticated", isUserAuthenticated())
  return (
    <Route
      {...rest}
      render={({ location }) =>
        isUserAuthenticated ? (
          children
        ) : (
          <Redirect to={{ pathname: urls.login, state: { from: location } }} />
        )
      }
    />
  )
}

const Routes = () => (
  <Switch>
    <Route exact path={urls.authorSignUp}>
      <AuthorSignUpForm />
    </Route>
    <PrivateRoute exact path={urls.books}>
      <BooksList />
    </PrivateRoute>
  </Switch>
)

export default Routes
