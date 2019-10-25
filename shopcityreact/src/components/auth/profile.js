import React, {Component} from 'react';
import { Link, withRouter } from 'react-router-dom';
import { connect } from 'react-redux';

import {updateUser} from '../../store/actions/authActions'


class Profile extends Component {
    state = {
        ...this.props.user
    }

    handleSubmit = (e) => {
        e.preventDefault()
        const { updateUser } = this.props;
        updateUser(this.state)
    }

    handleChange = (e) => {
        e.persist();
        this.setState({
            [e.target.id]: e.target.value
        });
    };

    render() {
        const { user, loginPending, updateError } = this.props;
        if (loginPending) {
            return (
                <div className="container user-">
                    <h4>You are not logged in... Please Login</h4>
                    <Link to="/login">Click here to Login</Link>
                </div>
            )
        }
        var error = <div className="update-error center-align"></div>
        if (updateError !== null) {
             error = <div className="update-error center-align red-text"><br/>Update Failed!</div>
        }
        return (
            <div className="container">
                <form onSubmit={this.handleSubmit}>
                    <h4 className="center">Profile</h4>
                    <div className="row">
                        <div className="input-field col s6">
                            <input value={this.state.firstName} id="firstName" type="text" className="validate" onChange={this.handleChange} required/>
                            <label className="active" htmlFor="firstName">First Name</label>
                        </div>
                        <div className="input-field col s6">
                            <input value={this.state.lastName} id="lastName" type="text" className="validate" onChange={this.handleChange} required/>
                            <label className="active" htmlFor="lastName">Last Name</label>
                        </div>
                    </div>
                    <div className="row">
                        <div className="input-field col s12">
                            <input value={this.state.username} id="username" type="text" className="validate" onChange={this.handleChange} required/>
                            <label className="active" htmlFor="username">Username</label>
                        </div>
                    </div>
                    <div className="row">
                        <div className="input-field col s12">
                            <input value={this.state.email} id="email" type="email" className="validate" onChange={this.handleChange} required/>
                            <label className="active" htmlFor="email">Email</label>
                        </div>
                    </div>
                    <div className="row">
                        <div className="input-field col s4">
                            <input value={this.state.city} id="city" type="text" className="validate" onChange={this.handleChange} required/>
                            <label className="active" htmlFor="city">City</label>
                        </div>
                        <div className="input-field col s4">
                            <input value={this.state.zipCode} id="zipCode" type="text" className="validate" onChange={this.handleChange} required/>
                            <label className="active" htmlFor="zipCode">Zip Code</label>
                        </div>
                        <div className="input-field col s4">
                            <input value={this.state.state} id="state" type="text" className="validate" onChange={this.handleChange} required/>
                            <label className="active" htmlFor="state">State</label>
                        </div>
                    </div>
                    <div className="row">
                        <div className="input-field col s12">
                            <input value={this.state.address} id="address" type="text" className="validate" onChange={this.handleChange} required/>
                            <label className="active" htmlFor="address">Address</label>
                        </div>
                    </div>
                    <div className="input-field center-align">
                        <button className="btn waves-effect waves-light" type="submit" name="action">Update</button>
                    </div>
                </form>
                {error}
            </div>
        )
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        updateUser: (user) => dispatch(updateUser(user))
    }
};

const mapStateToProps = (state) => {
    return {
        user: state.auth.user,
        loginPending: state.auth.loginPending,
        loginError: state.auth.loginError,
        updateError: state.auth.updateError
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(withRouter(Profile));
