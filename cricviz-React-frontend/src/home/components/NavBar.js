import React, { Component } from 'react';
import { OverlayTrigger, Popover, Navbar, Nav, NavItem, NavDropdown, MenuItem, FormGroup, FormControl, Button } from 'react-bootstrap';
import { BrowserRouter as Router, Route, Link, NavLink } from "react-router-dom";
import LoginForm from './LoginForm';
import SignUpForm from './SignupForm';
import SearchBar from '../containers/SearchBar';

const popoverLogin = (
  <Popover id="popover-login" title="Login Here">
    <LoginForm />
  </Popover>
);

const popoverSignUp = (
  <Popover id="popover-signup" title="SignUp Here">
    <SignUpForm />
  </Popover>
);

class NavBar extends Component {

  render() {
    return (
      <div>
        <Navbar className="navbar navbar-expand-lg bg-primary" bsStyle="default" collapseOnSelect>
          <Navbar.Header>
            <Navbar.Brand>
              <a href="#brand">CricViz</a>
            </Navbar.Brand>
            <Navbar.Toggle />
          </Navbar.Header>
          <Navbar.Collapse>
            <Nav pullLeft>
              <NavItem>
                <NavLink to="/" >
                  <Button className="btn btn-dark btn-outline-warning my-2 my-sm-0">Home</Button>
                </NavLink>
              </NavItem>
              <NavItem>
                <NavLink to="/live-scores" >
                  Live Scores
                </NavLink>
              </NavItem>
              <NavItem eventKey={3} href="#">
                <NavLink to="/player-insights" >
                  Player Insights
                </NavLink>
              </NavItem>
              <NavItem eventKey={4} href="#">
                <NavLink to="/follow-players" >
                  Follow Players
                </NavLink>
              </NavItem>
              <NavItem eventKey={5} href="#">
                <NavLink to="/follow-teams" >
                  Follow Teams
                </NavLink>
              </NavItem>
              <NavDropdown eventKey={6} title="Teams" id="basic-nav-dropdown">
                <MenuItem eventKey={6.1}>
                  <NavLink to="/teams-home">
                    Teams Home
                  </NavLink>
                </MenuItem>
                <MenuItem divider />
                <MenuItem eventKey={6.2}>Pakistan</MenuItem>
                <MenuItem eventKey={6.3}>India</MenuItem>
                <MenuItem eventKey={6.4}>Australia</MenuItem>
                <MenuItem eventKey={6.5}>England</MenuItem>
                <MenuItem eventKey={6.6}>South Africa</MenuItem>
                <MenuItem eventKey={6.7}>Srilanka</MenuItem>
                <MenuItem eventKey={6.8}>West Indies</MenuItem>
                <MenuItem eventKey={6.9}>Zimbabwe</MenuItem>
                <MenuItem eventKey={6.10}>Ireland</MenuItem>
              </NavDropdown>

            </Nav>
            <Nav pullRight>

                <OverlayTrigger trigger="click" rootClose placement="bottom" overlay={popoverLogin} >
                    <button type="button" className="btn btn-info" id="myLoginBtn">Login</button>
                </OverlayTrigger>

                <OverlayTrigger trigger="click" rootClose placement="bottom" overlay={popoverSignUp} >
                  <button type="button" className="btn btn-info" id="mySignUpBtn">Sign Up</button>
                </OverlayTrigger>

                <SearchBar />

            </Nav>
          </Navbar.Collapse>

        </Navbar>
      </div>
    );
  }

}

export default NavBar;
