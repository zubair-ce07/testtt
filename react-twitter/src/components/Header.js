import React from "react";
import {withRouter} from "react-router-dom";
import {MenuItem, Nav, Navbar, NavDropdown, NavItem} from "react-bootstrap";
import Link from "react-router-dom/es/Link";

const event = {
    news: 1,
    Menu: 2,
    profile:2.1,
    logout: 2.2,
};

class Header extends React.Component{
    constructor(props){
        super(props);
        this.handleSelect = this.handleSelect.bind(this);
    }
    handleSelect(eventKey) {
        if(eventKey===event.logout)
        {
            localStorage.clear();
            this.props.history.push('/');
        } else if (eventKey === event.news) {
            this.props.history.push('/news');
        }
    }

    render() {

        let loggedUserLinks = null;
        if (localStorage.user) {
            loggedUserLinks = (
                <Navbar.Collapse >
                    <Nav pullRight onSelect={this.handleSelect}>
                        <NavItem eventKey={event.news}>News</NavItem>
                        <NavDropdown eventKey={event.menu} title="Menu" id="basic-nav-dropdown">
                            <MenuItem eventKey={event.profile}>Profile</MenuItem>
                            <MenuItem divider/>
                            <MenuItem eventKey={event.logout}>Logout</MenuItem>
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
