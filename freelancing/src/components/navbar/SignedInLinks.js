import React from "react";
import { ROUTES } from "../../constants/routes";
import { MenuLink } from "./styles";

const SignedInLinks = ({ handleLogout }) => {
  return (
    <React.Fragment>
      <MenuLink to={ROUTES.SIGN_IN} button="true" onClick={handleLogout}>
        Logout
      </MenuLink>
    </React.Fragment>
  );
};

export default SignedInLinks;
