import React from 'react'
import {Link} from 'react-router-dom'
import {Navbar, NavItem, Nav} from 'react-bootstrap/lib'

class Navigation extends React.Component {

    render() {
        return (
            <Navbar inverse collapseOnSelect>
                <Navbar.Header>
                    <Navbar.Brand>
                        <a href="#">React-ToDo</a>
                    </Navbar.Brand>
                    <Navbar.Toggle/>
                </Navbar.Header>
                <Navbar.Collapse>

                    <Nav pullRight>
                        <NavItem eventKey={1}>
                            <Link to="/home">
                                Home
                            </Link>
                        </NavItem>
                        <NavItem eventKey={2}>
                            <Link to="/all">
                                Lists
                            </Link>
                        </NavItem>
                    </Nav>
                </Navbar.Collapse>
            </Navbar>
        )
    }
}
export default Navigation
