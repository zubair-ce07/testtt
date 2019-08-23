import React, { Component } from "react";
import { Route, Redirect } from "react-router-dom";
import { connect } from "react-redux";
import { loginUser } from "../../actions/user.actions";

import "./ProtectedRoute.css";

/**
 * TODO: Instead of routing to "/", route to original address after login.
 */

class ProtectedRoute extends Component {
  state = { redirect: false };

  componentDidMount = () => {
    const { loginUser } = this.props;
    const email = localStorage.getItem("email");
    const password = localStorage.getItem("password");
    if (email) {
      loginUser({ email, password });
    } else this.setState({ redirect: true });
  };

  render = () => {
    const { path, exact, component } = this.props;

    if (this.props.auth.isSignedIn)
      return <Route path={path} exact={exact} component={component} />;

    if (this.state.redirect) return <Redirect to="/login" />;

    return <h2>Logging in..</h2>;
  };
}

const mapStateToProps = state => {
  return { auth: state.auth };
};

export default connect(
  mapStateToProps,
  {
    loginUser
  }
)(ProtectedRoute);
