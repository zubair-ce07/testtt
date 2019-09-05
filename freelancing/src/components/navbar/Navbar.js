import React from "react";
import enhance from "./Navbar.enhancer";
import { Nav, NavHeader, NavRight, NavLeft, MenuLink, Logo } from "./styles";
import SignedOutLinks from "./SignedOutLinks";
import SignedInLinks from "./SignedInLinks";

const Navbar = ({ token, handleLogout }) => {
  return (
    <Nav>
      <NavHeader>
        <NavLeft>
          <Logo>Fiverr</Logo>
        </NavLeft>
        <NavRight>
          {token === null ? (
            <SignedOutLinks />
          ) : (
            <SignedInLinks handleLogout={handleLogout} />
          )}
        </NavRight>
      </NavHeader>
    </Nav>
  );
};

export default enhance(Navbar);
