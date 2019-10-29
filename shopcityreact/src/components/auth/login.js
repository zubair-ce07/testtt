import React, {Component} from 'react';
import { Link, withRouter } from 'react-router-dom';
import { connect } from 'react-redux';

import { authorizeUser, updateCart } from '../../store/actions/authActions';


class Login extends Component {
    state = {
        username: '',
        password: '',
        isAuthenticated: false,
        authorizationToken: ''
    };

    handleChange = (e) => {
        e.persist();
        this.setState({
            [e.target.id]: e.target.value
        });
    };

    handleSubmit = (e) => {
        e.preventDefault();
        const { authorizeUser } = this.props;
        authorizeUser(this.state);
    };

    redirect = () => {
        this.props.history.push('/');
    };

    render() {

        const { loginError, loginPending, registerPending, updateCart, user } = this.props;
        var registerSuccess = (
            <div className="register-success center-align"></div>
        );
        var error = <div className="login-error center-align"></div>;

        if (user.isAuthenticated && !user.isSuperUser) {
            updateCart(user);
        };
        if (!loginPending) {
            this.redirect();
        };
        if (!registerPending){
            registerSuccess = (
            <div className="register-success center-align green-text lighten-3">
                Successfully Registered!
            </div>
            );
        };
        if (loginError !== null) {
             error = (
                <div className="login-error center-align red-text">
                    {loginError.response.data.detail}<br/>
                    Login Failed! please enter correct username and password!
                </div>
             );
        };

        return (
            <div className="container">
                {registerSuccess}

                <form onSubmit={this.handleSubmit} className="white">
                    <h4 className="center">Login</h4>
                    <div className="input-field">
                        <input id="username" type="text" className="validate" onChange={this.handleChange} required/>
                        <label htmlFor="username">Username</label>
                    </div>
                    <div className="input-field">
                        <input id="password" type="password" className="validate" onChange={this.handleChange} required/>
                        <label htmlFor="password">Password</label>
                    </div>
                    <div className="input-field center-align">
                        <button className="btn waves-effect waves-light" type="submit" name="action">Login</button>
                    </div>
                </form>

                {error}
                <Link to="/register">Dont't have an account? Signup</Link>
            </div>
        );
    };
};


const mapDispatchToProps = (dispatch) => {
    return {
        authorizeUser: (user) => dispatch(authorizeUser(user)),
        updateCart: (user) => dispatch(updateCart(user))
    };
};


const mapStateToProps = (state) => {
    return {
        user: state.auth.user,
        loginPending: state.auth.loginPending,
        loginError: state.auth.loginError,
        registerPending: state.auth.registerPending
    };
};

export default connect(mapStateToProps, mapDispatchToProps)(withRouter(Login));
