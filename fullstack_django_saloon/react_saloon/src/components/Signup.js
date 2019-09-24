import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import { signup } from '../actions/userActions';
import PropTypes from 'prop-types';
import { reactAppConstants } from '../constants/constants';
import { routeConstants } from '../constants/routeConstants';

class Signup extends React.Component {

    state = {
        username: null,
        password1: null,
        password2: null,
        email: null,
        user_type: reactAppConstants.CUSTOMER
    }
    handleChange = e => {
        let nam = e.target.name;
        let val = e.target.value;
        this.setState({ [nam]: val });
    }
    handleSubmit = e => {
        e.preventDefault();
        this.props.signup(this.state.username, this.state.email, this.state.password1, this.state.password2, this.state.user_type).then(() => {
            if (!this.props.signupFailed) {
                this.props.history.push(routeConstants.LOGIN_ROUTE);
            }

        });
    }
    handleTabClick = e => {
        this.setState({ [reactAppConstants.USER_TYPE]: e.target.id });

    }

    render() {
        let tabClassCustomer = ['nav-link'];
        let tabClassSaloon = ['nav-link'];
        let passwordCheck = this.state.password1 === this.state.password2;
        if (this.state.user_type === reactAppConstants.CUSTOMER) {
            tabClassCustomer.push('active');
        }
        else {
            tabClassSaloon.push('active');
        }
        return (
            <div className='container'>
                {this.props.signupFailed &&
                    <div className="alert alert-danger" role="alert" >
                        Sign Up Failed!</div>}

                <div className="card" style={{ marginTop: '15%' }}>
                    <div className="card-body">
                        <center><h2>Sign Up</h2></center>
                        <ul className="nav nav-tabs">
                            <li style={{
                                width: '50%'
                            }} className="nav-item">
                                <Link className={tabClassCustomer.join(' ')} onClick={this.handleTabClick} id="customer" to="#">Customer
                                Registeration</Link>
                            </li>
                            <li style={{
                                width: '50%'
                            }} className=" nav-item">
                                <Link className={tabClassSaloon.join(' ')} id="saloon" onClick={this.handleTabClick} to="#">Saloon Registration</Link>
                            </li>
                        </ul>
                        <br />
                        <form onSubmit={this.handleSubmit}>
                            <div className="form-group">
                                <label htmlFor="exampleUsername">Username</label>
                                <input required type="text" className="form-control" onChange={this.handleChange} name='username' id="exampleUsername" aria-describedby="emailHelp" placeholder="Enter username" />
                            </div>
                            <div className="form-group">
                                <label htmlFor="exampleInputEmail1">Email</label>
                                <input required type="email" className="form-control" onChange={this.handleChange} name='email' id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="Enter Email" />
                            </div>
                            <div className="form-group">
                                <label htmlFor="exampleInputPassword1">Password</label>
                                <input required type="password" className="form-control" onChange={this.handleChange} name='password1' id="exampleInputPassword1" placeholder="Password" />
                            </div>
                            <div className="form-group">
                                <label htmlFor="exampleInputPassword2">Confrim Password</label>
                                <input required type="password" className="form-control" onChange={this.handleChange} name='password2' id="exampleInputPassword2" placeholder="Password" />
                                {!passwordCheck && <small style={{ color: 'red' }}>Password Does not match</small>}
                            </div>
                            {passwordCheck ? (
                                <button type="submit" value='customer' className="btn btn-primary">Sign Up</button>
                            ) : (
                                <button type="submit" value='customer' disabled className="btn btn-primary">Sign Up</button>
                            )}
                            <br /><br />
                            <Link to={routeConstants.LOGIN_ROUTE}>Login</Link>
                        </form>
                    </div>
                </div>
            </div >
        );
    }

}

Signup.propTypes = {
    signupFailed: PropTypes.bool.isRequired,
    signup: PropTypes.func.isRequired,
    history: PropTypes.object.isRequired
};

const mapStateToPropos = state =>
    (
        {
            signupFailed: state.user.signupFailed
        }
    );


const mapDispatchToProps = dispatch =>
    (
        {
            signup: (username, email, password1, password2, user_type) => dispatch(signup(username, email, password1, password2, user_type))
        }
    );

export default connect(mapStateToPropos, mapDispatchToProps)(Signup);