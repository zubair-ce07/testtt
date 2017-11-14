import React from 'react'
import {Navbar, NavItem, Nav} from 'react-bootstrap/lib'


const Navigation = (props) => {
    return(
        <Navbar inverse collapseOnSelect>
                <Navbar.Header>
                    <Navbar.Brand>
                        <a onClick={() => props.history.push('/')}>
                                React-ToDo
                        </a>
                    </Navbar.Brand>
                    <Navbar.Toggle/>
                </Navbar.Header>
                <Navbar.Collapse>

                    <Nav pullRight>
                        <NavItem eventKey={1} onClick={()=>props.history.push('/home')}>
                                Home
                        </NavItem>
                        <NavItem eventKey={2} onClick={()=>props.history.push('/todos')}>
                                Todos
                        </NavItem>
                    </Nav>
                </Navbar.Collapse>
            </Navbar>
    )
}

export default Navigation
