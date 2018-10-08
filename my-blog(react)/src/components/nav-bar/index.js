import React, { Component, Fragment } from 'react';
import { Link } from 'react-router-dom';

import {
  Collapse,
  Container,
  Navbar,
  NavbarToggler,
  NavbarBrand,
  Nav,
  NavItem,
  NavLink
} from 'reactstrap';

import userContainer from '../users/container';


class NavBar extends Component {
  constructor(props) {
    super(props);

    this.toggle = this.toggle.bind(this);
    this.state = {
      isOpen: false
    };
  }
  toggle() {
    this.setState({
      isOpen: !this.state.isOpen
    });
  }
  render() {
    const isSignedIn = Boolean(this.props.user.username);

    return (
      <Navbar color='dark' dark expand='md' fixed={'top'}>
        <Container>
          <NavbarBrand tag={Link} to='/'>My Blog</NavbarBrand>
          <NavbarToggler onClick={this.toggle} />
          <Collapse isOpen={this.state.isOpen} navbar>
            <Nav className='ml-auto' navbar>
              {
                isSignedIn ?
                  <Fragment>
                    <NavItem>
                      <NavLink tag={Link} to='/blogs/create'>
                        Create Blog
                      </NavLink>
                    </NavItem>
                    <NavItem>
                      <NavLink tag={Link} to='/users/profile'>
                        Profile
                      </NavLink>
                    </NavItem>
                    <NavItem>
                      <NavLink onClick={this.props.signOut} href='#'>Sign Out</NavLink>
                    </NavItem>
                  </Fragment>
                  :
                  <Fragment>
                    <NavItem>
                      <NavLink tag={Link} to='/users/signup'>Sign Up</NavLink>
                    </NavItem>
                    <NavItem>
                      <NavLink tag={Link} to='/users/signin'>Sign In</NavLink>
                    </NavItem>
                  </Fragment>
              }
            </Nav>
          </Collapse>
        </Container>
      </Navbar>
    );
  }
}

export default userContainer(NavBar);
