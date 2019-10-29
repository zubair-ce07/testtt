import React, {Component} from 'react';
import { Link} from 'react-router-dom';
import { connect } from 'react-redux';

import { registerUser } from '../../store/actions/authActions'


class Register extends Component {
    state = {
        first_name: '',
        last_name: '',
        username: '',
        email: '',
        city: '',
        zip_code: '',
        state: '',
        address: '',
        password: '',
        confirm_password: '',
    };

    handleChange = (e) => {
        e.persist();
        this.setState({
            [e.target.id]: e.target.value
        });
    };

    handleSubmit = (e) => {
        e.preventDefault();
        this.props.registerUser(this.state);
    };

    render() {
        const { registerError, registerPending } = this.props;
        var error = <div className="register-error center-align"></div>

        if (!registerPending) {
            this.props.history.push('/login');
        }; 
        if (registerError !== null) {
             error = (
                <div className="register-error center-align red-text">
                    {registerError.response.request.response}<br/>
                    Registration Failed!
                </div>
             );
        }

        return (
            <div className="container">
                <form onSubmit={this.handleSubmit}>
                    <h4 className="center">Register!</h4>
                    <div className="row">
                        <div className="input-field col s6">
                            <input id="first_name" type="text" className="validate" onChange={this.handleChange} required/>
                            <label htmlFor="first_name">
                                First Name
                            </label>
                        </div>
                        <div className="input-field col s6">
                            <input id="last_name" type="text" className="validate" onChange={this.handleChange} required/>
                            <label htmlFor="last_name">
                                Last Name
                            </label>
                        </div>
                    </div>
                    <div className="row">
                        <div className="input-field col s12">
                            <input id="username" type="text" className="validate" onChange={this.handleChange} required/>
                            <label htmlFor="username">
                                Username
                            </label>
                        </div>
                    </div>
                    <div className="row">
                        <div className="input-field col s12">
                            <input id="email" type="email" className="validate" onChange={this.handleChange} required/>
                            <label htmlFor="email">
                                Email
                            </label>
                        </div>
                    </div>
                    <div className="row">
                        <div className="input-field col s4">
                            <input id="city" type="text" className="validate" onChange={this.handleChange} required/>
                            <label htmlFor="city">
                                City
                            </label>
                        </div>
                        <div className="input-field col s4">
                            <input id="zip_code" type="text" className="validate" onChange={this.handleChange} required/>
                            <label htmlFor="zipcode">
                                Zip Code
                            </label>
                        </div>
                        <div className="input-field col s4">
                            <input id="state" type="text" className="validate" onChange={this.handleChange} required/>
                            <label htmlFor="state">
                                State
                            </label>
                        </div>
                    </div>
                    <div className="row">
                        <div className="input-field col s12">
                            <input id="address" type="text" className="validate" onChange={this.handleChange} required/>
                            <label htmlFor="address">
                                Address
                            </label>
                        </div>
                    </div>
                    <div className="row">
                        <div className="input-field col s12">
                            <input id="password" type="password" className="validate" onChange={this.handleChange} required/>
                            <label htmlFor="password">
                                Password
                            </label>
                        </div>
                    </div>
                    <div className="row">
                        <div className="input-field col s12">
                            <input id="confirm_password" type="password" className="validate" onChange={this.handleChange} required/>
                            <label htmlFor="confirm_password">
                                Re-Enter Password
                            </label>
                        </div>
                    </div>
                    <div className="input-field center-align">
                        <button className="btn waves-effect waves-light" type="submit" name="action">
                            Signup
                        </button>
                    </div>
                </form>
                {error}
                <Link to="/login">
                    Already have an account? Login
                </Link>
            </div>
        );
    };
};


const mapDispatchToProps = (dispatch) => {
    return {
        registerUser: (user) => dispatch(registerUser(user))
    };
};


const mapStateToProps = (state) => {
    return {
        user: state.auth.user,
        registerPending: state.auth.registerPending,
        registerError: state.auth.registerError
    };
};

export default connect(mapStateToProps, mapDispatchToProps)(Register);
