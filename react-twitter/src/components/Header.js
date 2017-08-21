import React from "react";
import {Link, withRouter} from "react-router-dom";
import {MenuItem, Nav, Navbar, NavDropdown, NavItem} from "react-bootstrap";

const event = {
    NEWS: 1,
    MENU: 2,
    PROFILE:2.1,
    LOGOUT: 2.2,
};

class Header extends React.Component{
    constructor(props){
        super(props);
        this.handleSelect = this.handleSelect.bind(this);
    }
    handleSelect(eventKey) {
        if(eventKey===event.LOGOUT)
        {
            localStorage.clear();
            this.props.history.push('/');
        } else if (eventKey === event.NEWS) {
            this.props.history.push('/news');
        }
    }

    render() {
        let loggedUserLinks = localStorage.user ? (
                <Navbar.Collapse >
                    <Nav pullRight onSelect={this.handleSelect}>
                        <NavItem eventKey={event.NEWS}>News</NavItem>
                        <NavDropdown eventKey={event.MENU} title="Menu" id="basic-nav-dropdown">
                            <MenuItem eventKey={event.PROFILE}>Profile</MenuItem>
                            <MenuItem divider/>
                            <MenuItem eventKey={event.LOGOUT}>Logout</MenuItem>
                        </NavDropdown>
                    </Nav>
                </Navbar.Collapse>
        ) : null;


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
