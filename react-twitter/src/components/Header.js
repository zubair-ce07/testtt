import React from "react";
import {withRouter} from "react-router-dom";
import {MenuItem, Nav, Navbar, NavDropdown, NavItem} from "react-bootstrap";
import Link from "react-router-dom/es/Link";


class Header extends React.Component{
    constructor(props){
        super(props);
        this.handleSelect = this.handleSelect.bind(this);
    }
    handleSelect(eventKey) {
        if(eventKey===3.2)
            this.props.history.push('/logout');
    }

    render() {

        let loggedUserLinks = null;
        if (localStorage.user) {
            loggedUserLinks = (
                <Navbar.Collapse >
                    <Nav pullRight onSelect={this.handleSelect}>
                        <NavItem eventKey={1} href="#">News</NavItem>
                        <NavDropdown eventKey={2} title="Dropdown" id="basic-nav-dropdown">
                            <MenuItem eventKey={2.1}>Profile</MenuItem>
                            <MenuItem divider/>
                            <MenuItem eventKey={3.2}>Logout</MenuItem>
                        </NavDropdown>
                    </Nav>
                </Navbar.Collapse>
            );
        }

        return (
            <Navbar inverse collapseOnSelect>
                <Navbar.Header>
                    <Navbar.Brand>
                        <Link to="/" >Tweeter</Link>
                    </Navbar.Brand>
                    <Navbar.Toggle />
                </Navbar.Header>
                {loggedUserLinks}
            </Navbar>

        );
    }
}

export default withRouter(Header);
