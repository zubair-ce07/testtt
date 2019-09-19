import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import { signup } from '../actions/userActions';
import PropTypes from 'prop-types';

class Signup extends React.Component {

    state = {
        username: null,
        password1: null,
        password2: null,
        email: null,
        user_type: 'customer'
    }
    handleChange = (e) => {
        let nam = e.target.name;
        let val = e.target.value;
        this.setState({ [nam]: val });
    }
    handleSubmit = (e) => {
        e.preventDefault();
        this.props.signup(this.state.username, this.state.email, this.state.password1, this.state.password2, this.state.user_type).then(() => {
            if (!this.props.signup_failed) {
                this.props.history.push('/login');
            }

        });
    }
    handleTabClick = (e) => {
        this.setState({ user_type: e.target.id });

    }

    render() {
        let tab_class_customer = ['nav-link'];
        let tab_class_saloon = ['nav-link'];
        if (this.state.user_type === 'customer') {
            tab_class_customer.push('active');
        }
        else {
            tab_class_saloon.push('active');
        }
        return (
            <div className='container'>
                {this.props.signup_failed &&
                    <div className="alert alert-danger" role="alert" >
                        Sign Up Failed!</div>}

                <div className="card" style={{ marginTop: '15%' }}>
                    <div className="card-body">
                        <center><h2>Sign Up</h2></center>
                        <ul className="nav nav-tabs">
                            <li style={{
                                width: '50%'
                            }} className="nav-item">
                                <Link className={tab_class_customer.join(' ')} onClick={this.handleTabClick} id="customer" to="#">Customer
                                Registeration</Link>
                            </li>
                            <li style={{
                                width: '50%'
                            }} className=" nav-item">
                                <Link className={tab_class_saloon.join(' ')} id="saloon" onClick={this.handleTabClick} to="#">Saloon Registration</Link>
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
                                <small></small>
                            </div>
                            <button type="submit" value='customer' className="btn btn-primary">Sign Up</button>
                            <br /><br />
                            <Link to='/login'>Login</Link>
                        </form>
                    </div>
                </div>
            </div >
        );
    }

}

Signup.propTypes = {
    signup_failed: PropTypes.bool.isRequired,
    signup: PropTypes.func.isRequired,
    history:PropTypes.object.isRequired
};

const mapStateToPropos = (state) => {
    return {
        signup_failed: state.user.signup_failed
    };
};

const mapDispatchToProps = dispatch => {
    return {
        signup: (username, email, password1, password2, user_type) => dispatch(signup(username, email, password1, password2, user_type))
    };
};

export default connect(mapStateToPropos, mapDispatchToProps)(Signup);