import React, { Component } from "react";
import { Router, Route, Switch } from "react-router-dom";
import { connect } from "react-redux";

import ProtectedRoute from "../ProtectedRoute/ProtectedRoute";

import { attemptLogin } from "../../actions/auth.actions";
import history from "../../history";

import Home from "../Home/Home";
import LoginForm from "../LoginForm/LoginForm";
import RegisterForm from "../RegisterForm/RegisterForm";
import ProfilePage from "../ProfilePage/ProfilePage";

import "../styles.css";
import "./App.css";

class App extends Component {
  componentDidMount = () => {
    this.props.attemptLogin();
  };

  render = () => {
    const { isSignedIn } = this.props.auth;
    return (
      <Router history={history}>
        <Switch>
          <ProtectedRoute
            path="/register"
            exact
            component={RegisterForm}
            redirect="/"
            condition={isSignedIn}
          />
          <ProtectedRoute
            path="/login"
            exact
            component={LoginForm}
            redirect="/"
            condition={isSignedIn}
          />
          <ProtectedRoute
            path="/"
            exact
            component={Home}
            redirect="/login"
            condition={!isSignedIn}
          />
          <Route path="/user/:id" exact component={ProfilePage} />
        </Switch>
      </Router>
    );
  };
}

const mapStateToProps = state => {
  return { auth: state.auth };
};

export default connect(
  mapStateToProps,
  { attemptLogin }
)(App);
