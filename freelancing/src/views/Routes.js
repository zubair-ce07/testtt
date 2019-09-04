import React from "react";
import { Route } from "react-router-dom";
import { ROUTES } from "../constants/routes";
import SignIn from "../components/auth/SignIn";
import SignUp from "../components/auth/SignUp";

const Routes = () => {
  return (
    <React.Fragment>
      <Route path={ROUTES.SIGN_IN} component={SignIn} />
      <Route path={ROUTES.SIGN_UP} component={SignUp} />
    </React.Fragment>
  );
};

export default Routes;
