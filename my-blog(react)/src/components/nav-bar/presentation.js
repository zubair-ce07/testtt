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


class NavBar extends Component {
  state = { isOpen: false };

  componentDidMount() {
    if (localStorage.getItem('user')) {
      this.props.initialize();
    }
  }
  toggle = () => {
    this.setState({
      isOpen: !this.state.isOpen
    });
  }
  render() {
    const isSignedIn = Boolean(this.props.user.id);

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
                      <NavLink onClick={this.props.signOut} href='#'>
                        Sign Out
                      </NavLink>
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

export default NavBar;
