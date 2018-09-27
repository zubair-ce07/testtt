import React, { Component } from 'react';
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
    return (
      <Navbar color='dark' dark expand='md'>
        <Container>
          <NavbarBrand tag={Link} to='/'>My Blog</NavbarBrand>
          <NavbarToggler onClick={this.toggle} />
          <Collapse isOpen={this.state.isOpen} navbar>
            <Nav className='ml-auto' navbar>
              <NavItem>
                <NavLink tag={Link} to='/blogs/create'>Create Blog</NavLink>
              </NavItem>
              <NavItem>
                <NavLink tag={Link} to='/users/profile'>Profile</NavLink>
              </NavItem>
              <NavItem>
                <NavLink tag={Link} to='/users/signup'>Sign Up</NavLink>
              </NavItem>
              <NavItem>
                <NavLink tag={Link} to='/users/signin'>Sign In</NavLink>
              </NavItem>
            </Nav>
          </Collapse>
        </Container>
      </Navbar>
    );
  }
}

export default NavBar;
