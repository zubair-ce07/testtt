import React from "react";
import { Route } from "react-router-dom";
import { ROUTES } from "../constants/routes";
import SignIn from "../components/auth/SignIn";
import SignUp from "../components/auth/SignUp";

const Routes = () => {
  return (
    <React.Fragment>
      <Route
        path={ROUTES.SIGN_IN}
        render={props => <SignIn {...props} title="Login To Fiverr" />}
      />
      <Route
        path={ROUTES.SIGN_UP}
        render={props => <SignUp {...props} title="Join Fiverr" />}
      />
    </React.Fragment>
  );
};

export default Routes;
