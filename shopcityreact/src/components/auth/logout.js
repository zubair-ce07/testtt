import React, {Component} from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';

import {unauthorizeUser} from '../../store/actions/authActions'


class Logout extends Component {
    handleLogout = () => {
        let user = {
            username: '',
            password: '',
            isAuthenticated: false,
            authorizationToken: ''
        }
        this.props.unauthorizeUser(user)
    }
    render() {
        if (this.props.user.isAuthenticated) {
            this.handleLogout()
        }
        return (
            <div className="container">
                <h4>Thank You for Shopping with Us!!</h4>
                <li><Link to="/login">Login Again?</Link></li>
            </div>
        )
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        unauthorizeUser: (user) => dispatch(unauthorizeUser(user))
    }
};

const mapStateToProps = (state) => {
    return {
        user: state.auth.user
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(Logout);
