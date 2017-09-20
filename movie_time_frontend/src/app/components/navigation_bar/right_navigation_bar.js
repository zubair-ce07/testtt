import React, {Component} from 'react';
import {connect} from 'react-redux';
import {NavItem, Nav, NavDropdown, DropdownItem, DropdownToggle, DropdownMenu} from 'reactstrap'

import NotificationDropDown from './notifications_dorpdown';
import RequestsDropDown from './requests_dropdown';
import {logout} from '../../actions/auth_actions';
import {Link} from "react-router-dom";


class RightNavBar extends Component {
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

    logout() {
        this.props.logout();
    }

    static renderGuestLinks() {
        return (
            <Nav className="ml-auto" navbar>
                <NavItem>
                    <Link className="nav-link" to="/signup/"><i className="fa fa-user-plus"/> Sign up</Link>
                </NavItem>
                <NavItem>
                    <Link className="nav-link" to="/login/"><i className="fa fa-sign-in"/> Login</Link>
                </NavItem>
            </Nav>
        );
    }

    renderUserLinks(user) {
        return (
            <NavDropdown isOpen={this.state.isOpen} toggle={this.toggle}>
                <DropdownToggle nav><img className="rounded-circle"
                                         src={user.photo === null ? '/images/avatar.jpg' : user.photo} width={27}
                                         height={27}/> {user.first_name} {user.last_name} <i
                    className="fa fa-chevron-circle-down"/></DropdownToggle>
                <DropdownMenu right>
                    <DropdownItem><Link className="nav-link" to={`/users/${user.id}/`}>
                        <i className="fa fa-user"/> Profile</Link></DropdownItem>
                    <DropdownItem divider/>
                    <DropdownItem><Link className="nav-link" to="/login/" onClick={this.logout.bind(this)}><i
                        className="fa fa-sign-out"/> Logout</Link></DropdownItem>
                </DropdownMenu>
            </NavDropdown>
        );
    }

    render() {
        let panel = null;
        if (!this.props.auth_user.isAuthenticated)
            panel = this.constructor.renderGuestLinks();
        else
            panel = (
                <Nav className="ml-auto" navbar>
                    <RequestsDropDown/>
                    <NotificationDropDown/>
                    {this.renderUserLinks(this.props.auth_user.user)}
                </Nav>
            );
        return panel;
    }
}

export default connect(null, {logout})(RightNavBar);
