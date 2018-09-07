import React, { Component } from 'react';
import { OverlayTrigger, Popover, Navbar, Nav, NavItem, NavDropdown, MenuItem, FormGroup, FormControl, Button } from 'react-bootstrap';
import { BrowserRouter as Router, Route, Link, NavLink } from "react-router-dom";


const popoverLogin = (
  <Popover id="popover-trigger-click-root-close" title="Login Here">
    <form>
      <label>
        UserName:
        <input type="text" name="username" />
      </label>
      <label>
        Password:
        <input type="password" name="password" />
      </label>
      <input type="submit" value="Login" />
    </form>
  </Popover>
);

const popoverSignUp = (
  <Popover id="popover-trigger-click-root-close" title="SignUp Here">
    <form>
      <label>
        UserName:
        <input type="text" name="username" />
      </label>
      <label>
        Password:
        <input type="password" name="password1" />
      </label>
      <label>
        Repeat Password:
        <input type="password" name="password2" />
      </label>
      <input type="submit" value="SignUp" />
    </form>
  </Popover>
);

class NavBar extends Component {

  render() {
    return (
      <div>
        <Navbar className="navbar navbar-expand-lg bg-primary" bsStyle="primary" collapseOnSelect>
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
                <NavLink to="/playepopoverClickRootCloser-insights" >
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

                <FormGroup>
                  <FormControl type="text" placeholder="Search for players/teams" />
                </FormGroup>{' '}
                <Button className="btn btn-dark btn-outline-warning my-2 my-sm-0" bsStyle="primary" type="submit" >Search</Button>

                <OverlayTrigger
                  trigger="click"
                  rootClose
                  placement="bottom"
                  overlay={popoverLogin}
                >
                    <button type="button" className="btn btn-info" id="myLoginBtn">Login</button>
                </OverlayTrigger>

                <OverlayTrigger
                  trigger="click"
                  rootClose
                  placement="bottom"
                  overlay={popoverSignUp}
                >
                  <button type="button" className="btn btn-info" id="mySignUpBtn">Sign Up</button>
                </OverlayTrigger>

            </Nav>
          </Navbar.Collapse>

        </Navbar>
      </div>
    );
  }

}

const Home = () => (
  <div>
    <h2 >Home</h2>
    <h2>Home</h2>
    <h2>Home</h2>
    <h2>Home</h2>
  </div>
);

const LiveScores = () => (
  <div>
    <h2>Live Scores</h2>
  </div>
);

const PlayerInsights = () => (
  <div>
    <h2>Player Insights</h2>

  </div>
);

const FollowPlayers = () => (
  <div>
    <h2>Follow Players</h2>
  </div>
);

const FollowTeams = () => (
  <div>
    <h2>Follow Teams</h2>
  </div>
);

const TeamsHome = () => (
  <div>
    <h2>Teams Home</h2>
  </div>
);


export default NavBar;
