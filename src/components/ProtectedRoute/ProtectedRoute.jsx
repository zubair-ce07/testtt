import React, { Component } from "react";
import { Route, Redirect } from "react-router-dom";
import { connect } from "react-redux";
import { loginUser } from "../../actions/auth.actions";

import "./ProtectedRoute.css";

/**
 * TODO: Instead of routing to "/", route to original address after login.
 */

class ProtectedRoute extends Component {
  state = { redirect: false };

  componentDidMount = () => {
    // this.props.loginUser({ email: "ali@mail.com", password: "12345678" });
  };

  render = () => {
    const { path, exact, component } = this.props;

    if (!this.props.auth.isSignedIn) return <Redirect to="/login" />;

    return <Route path={path} exact={exact} component={component} />;
  };
}

const mapStateToProps = state => {
  return { auth: state.auth };
};

export default connect(
  mapStateToProps,
  { loginUser }
)(ProtectedRoute);
