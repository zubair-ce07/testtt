import React, {Component} from "react";
import {connect} from "react-redux";
import {browserHistory} from "react-router";
import {bindActionCreators} from "redux";
import {logout} from "../actions";

class Logout extends Component {
    componentWillMount() {
        if (!localStorage.getItem('token')) {
            browserHistory.push('/');
        };
    };
    render() {
        return (
            <li onClick={
                (e) => {
                    e.preventDefault();
                    this.props.logout(localStorage.getItem('token')).then(() => {
                        browserHistory.push('/')
                    });
                }}><a className="dropdown-button waves-effect waves-dark" href="">
                <i className="fa fa-sign-out fa-fw"></i> <b>Logout</b> </a>
            </li>
        );
    };
}
function mapDispatchToProps(dispatch) {
    return bindActionCreators(
        {
            logout: logout
        }, dispatch);
};
export default connect(null, mapDispatchToProps)(Logout);
