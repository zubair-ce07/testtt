import { Redirect, Route, Switch } from "react-router-dom"
import { checkAdminUser, getAuthTokenCookie } from "./util/utils"

import AuthorDetail from "./components/AuthorDetail"
import AuthorSignUpForm from "./components/AuthorSignUpForm"
import AuthorsList from "./components/AuthorsList"
import BookDetail from "./components/BookDetail"
import BookForm from "./components/BookForm"
import BooksList from "./components/BooksList"
import CategoriesList from "./components/CategoriesList"
import LogInForm from "./components/LogInForm"
import NoMatch from "./components/NotFound"
import PublisherDetail from "./components/PublisherDetail"
import PublisherSignUpForm from "./components/PublisherSignUpForm"
import PublishersList from "./components/PublishersList"
import React from "react"
import urls from "./urls"

const isUserAuthenticated = () => {
  return Boolean(getAuthTokenCookie())
}

const isAdminUser = () => {
  return Boolean(checkAdminUser())
}

const customRoute = (condition, redirect_path, { children, ...rest }) => {
  return (
    <Route
      {...rest}
      render={({ location }) =>
        condition ? (
          children
        ) : (
          <Redirect
            to={{ pathname: redirect_path, state: { from: location } }}
          />
        )
      }
    />
  )
}

const ProtectedRoute = ({ children, ...rest }) => {
  // For logged in users
  return customRoute(isUserAuthenticated(), urls.login, { children, ...rest })
}

const PrivateRoute = ({ children, ...rest }) => {
  // Only for Admins
  return customRoute(isAdminUser(), urls.home, { children, ...rest })
}

const PublicRoute = ({ children, ...rest }) => {
  // No need for login
  return customRoute(!isUserAuthenticated(), urls.home, { children, ...rest })
}

const Routes = () => (
  <Switch>
    <PublicRoute exact path={urls.authorSignUp}>
      <AuthorSignUpForm />
    </PublicRoute>
    <PublicRoute exact path={urls.publisherSignUp}>
      <PublisherSignUpForm />
    </PublicRoute>
    <PublicRoute exact path={urls.login}>
      <LogInForm />
    </PublicRoute>

    <ProtectedRoute exact path={urls.home}>
      <Redirect to={urls.books} />
    </ProtectedRoute>
    <ProtectedRoute exact path={urls.books}>
      <BooksList />
    </ProtectedRoute>
    <ProtectedRoute exact path={urls.bookDetail}>
      <BookDetail />
    </ProtectedRoute>

    <ProtectedRoute exact path={urls.authors}>
      <AuthorsList />
    </ProtectedRoute>
    <ProtectedRoute exact path={urls.authorDetail}>
      <AuthorDetail />
    </ProtectedRoute>

    <ProtectedRoute exact path={urls.publishers}>
      <PublishersList />
    </ProtectedRoute>
    <ProtectedRoute exact path={urls.publisherDetail}>
      <PublisherDetail />
    </ProtectedRoute>

    <ProtectedRoute exact path={urls.categories}>
      <CategoriesList />
    </ProtectedRoute>

    <PrivateRoute exact path={urls.bookNew}>
      <BookForm />
    </PrivateRoute>
    <PrivateRoute exact path={urls.bookEdit}>
      <BookForm edit />
    </PrivateRoute>

    <Route path="*">
      <NoMatch />
    </Route>
    <Route exact path={urls.notFound}>
      <NoMatch />
    </Route>
  </Switch>
)

export default Routes
