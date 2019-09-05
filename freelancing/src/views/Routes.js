import React from "react";
import { Route } from "react-router-dom";
import { ROUTES } from "../constants/routes";
import SignIn from "../components/auth/SignIn";
import SignUp from "../components/auth/SignUp";
import Buyer from "./buyer/Buyer";

const Routes = () => {
  return (
    <React.Fragment>
      <Route exact path={ROUTES.ROOT} component={Buyer} />
      <Route exact path={ROUTES.SIGN_IN} component={SignIn} />
      <Route exact path={ROUTES.SIGN_UP} component={SignUp} />
    </React.Fragment>
  );
};

export default Routes;
