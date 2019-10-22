import React from "react";

import Navbar from "react-bootstrap/Navbar";
import NavDropdown from "react-bootstrap/NavDropdown";

import { api } from "../.././utils/api";

function logout() {
  api
    .post(`logout/`)
    .then(({ data }) => {
      localStorage.clear();
      window.location.href = "/";
    })
    .catch(error => {
      console.log("error", error);
      // todo show toast
    });
}

export const Header = () => (
  <Navbar bg="dark" variant="dark">
    <Navbar.Brand href="#home">Navbar with text</Navbar.Brand>
    <Navbar.Toggle />
    <Navbar.Collapse className="justify-content-end">
      <Navbar.Text>Signed in as:</Navbar.Text>
      <NavDropdown title="Mark Otto" id="collasible-nav-dropdown">
        <NavDropdown.Item>Profile</NavDropdown.Item>
        <NavDropdown.Item onClick={logout}>Logout</NavDropdown.Item>
        <NavDropdown.Divider />
      </NavDropdown>
    </Navbar.Collapse>
  </Navbar>
);
