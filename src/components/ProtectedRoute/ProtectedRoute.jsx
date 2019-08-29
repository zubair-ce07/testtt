import React from "react";
import { Route, Redirect } from "react-router-dom";

import "./ProtectedRoute.css";

const ProtectedRoute = ({ path, exact, component, redirect, condition }) => {
  if (condition) return <Redirect to={redirect} />;
  return <Route path={path} exact={exact} component={component} />;
};

export default ProtectedRoute;

/**
 * TODO: Instead of routing to "/", route to original address after login.
 * */
