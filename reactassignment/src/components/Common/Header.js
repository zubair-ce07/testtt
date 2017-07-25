import React from 'react'
import {Link} from 'react-router-dom'

import {Navbar, NavItem, Nav, Button} from 'react-bootstrap/lib'

class Navigation extends React.Component {
    render() {
        return (
            <Navbar inverse collapseOnSelect>
                <Navbar.Header>
                    <Navbar.Brand>
                        <a onClick={() => this.props.history.push('/')}>
                                React-ToDo
                        </a>
                    </Navbar.Brand>
                    <Navbar.Toggle/>
                </Navbar.Header>
                <Navbar.Collapse>

                    <Nav pullRight>
                        <NavItem eventKey={1} onClick={()=>this.props.history.push('/home')}>
                                Home
                        </NavItem>
                        <NavItem eventKey={2} onClick={()=>this.props.history.push('/todos')}>
                                Todos
                        </NavItem>
                    </Nav>
                </Navbar.Collapse>
            </Navbar>
        )
    }
}

export default Navigation
