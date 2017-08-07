import React from 'react'
import {Nav, Navbar, NavItem} from 'react-bootstrap'
import * as auth from '../authentication/auth'

const Navigation = (props) => {
    let divStyle= {
        'fontFamily': ('Permanent Marker'),
        'fontSize': '48px',
        'cursor': 'pointer'
    }
    return(
        <Navbar inverse collapseOnSelect>
                <Navbar.Header>
                    <Navbar.Brand>
                        <a onClick={() => props.history.push('/')} style={divStyle}>
                                Super Store
                        </a>
                    </Navbar.Brand>
                    <Navbar.Toggle/>
                </Navbar.Header>
                <Navbar.Collapse>
                    <Nav>
                        <NavItem eventKey={1} onClick={()=>props.history.push('/home/brands')}>
                                Home
                        </NavItem>
                        <NavItem eventKey={2} onClick={()=>props.history.push('/home/products')}>
                                All Products
                        </NavItem>
                    </Nav>
                    <Nav pullRight>
                        <NavItem eventKey={3} onClick={() => {auth.logout(); props.history.push('/app/login/')}}>
                                Logout
                        </NavItem>
                    </Nav>
                </Navbar.Collapse>
            </Navbar>
    )
}

export default Navigation
