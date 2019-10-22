import React, {Component} from 'react';
import { Link, withRouter } from 'react-router-dom';
import { connect } from 'react-redux';

// import {setUserName, setPassword, setIsAuthenticated, setAuthorizationToken} from '../../store/actions/authActions'
import {authorizeUser} from '../../store/actions/authActions'


class Login extends Component {
    state = {
        username: '',
        password: '',
        isAuthenticated: false,
        authorizationToken: ''
    }
    handleChange = (e) => {
        e.persist();
        this.setState({
            [e.target.id]: e.target.value
        })
    }
    handleSubmit = (e) => {
        e.preventDefault();
        this.props.authorizeUser(this.state)
        this.props.history.push('/');
    }
    render() {
        return (
            <div className="container">
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
                    <Link to="/register">Dont't have an account? Signup</Link>
                </form>
            </div>
        )
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        authorizeUser: (user) => dispatch(authorizeUser(user))
    }
};

const mapStateToProps = (state) => {
    return {
        user: state.auth.user
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(withRouter(Login));
