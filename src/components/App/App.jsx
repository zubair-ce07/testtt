import React, { Component } from "react";
import { Router, Route, Switch } from "react-router-dom";

import ProtectedRoute from "../ProtectedRoute/ProtectedRoute";

import history from "../../history";

import Home from "../Home/Home";
import LoginForm from "../LoginForm/LoginForm";
import RegisterForm from "../RegisterForm/RegisterForm";
import ProfilePage from "../ProfilePage/ProfilePage";

import "../styles.css";
import "./App.css";

class App extends Component {
  state = {};

  render = () => {
    return (
      <Router history={history}>
        <Switch>
          <Route path="/register" exact component={RegisterForm} />
          <Route path="/login" exact component={LoginForm} />
          <ProtectedRoute path="/" exact component={Home} />
          <Route path="/user/:id" exact component={ProfilePage} />
        </Switch>
      </Router>
    );
  };
}

export default App;
