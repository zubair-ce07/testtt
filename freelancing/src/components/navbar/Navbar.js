import React from "react";
import { Nav, NavHeader, NavRight, NavLeft, MenuLink, Logo } from "./styles";
import { ROUTES } from "../../constants/routes";

const Navbar = () => {
  return (
    <Nav>
      <NavHeader>
        <NavLeft>
          <Logo>Fiverr</Logo>
        </NavLeft>
        <NavRight>
          <MenuLink to={ROUTES.SIGN_IN}>Sign In</MenuLink>
          <MenuLink to={ROUTES.SIGN_UP} button="true">
            Join
          </MenuLink>
        </NavRight>
      </NavHeader>
    </Nav>
  );
};

export default Navbar;
