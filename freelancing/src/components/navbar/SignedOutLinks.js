import React from "react";
import { ROUTES } from "../../constants/routes";
import { MenuLink } from "./styles";

const SignedOutLinks = () => {
  return (
    <React.Fragment>
      <MenuLink to={ROUTES.SIGN_IN}>Sign In</MenuLink>
      <MenuLink to={ROUTES.SIGN_UP} button="true">
        Join
      </MenuLink>
    </React.Fragment>
  );
};

export default SignedOutLinks;
