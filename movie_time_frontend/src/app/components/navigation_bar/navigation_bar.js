import React, {Component} from 'react';
import {connect} from 'react-redux';
import {Collapse, Navbar, NavbarToggler, NavbarBrand} from 'reactstrap';

import RightNavBar from './right_navigation_bar';
import {Link} from "react-router-dom";

class NavigationBar extends Component {
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
            <div>
                <Navbar color="primary" fixed="top" toggleable inverse>
                    <NavbarToggler right onClick={this.toggle}/>
                    <Link className="navbar-brand" to="/"><i className="fa fa-ticket"/> Movie Time</Link>
                    <Collapse isOpen={this.state.isOpen} navbar>
                        <RightNavBar auth_user={this.props.auth_user}/>
                    </Collapse>
                </Navbar>
            </div>
        );
    }
}

function mapStateToProps({auth_user}) {
    return {auth_user};
}

export default connect(mapStateToProps)(NavigationBar);
