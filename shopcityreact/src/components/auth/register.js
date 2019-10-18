import React from 'react';
import { Link} from 'react-router-dom';


const Register = () => {
    return (
        <div className="container">
            <form>
                <h4 className="center">Register!</h4>
                <div className="row">
                    <div className="col s6">
                        <input id="first_name" type="text" className="validate" required/>
                        <label htmlFor="first_name">First Name</label>
                    </div>
                    <div className="col s6">
                        <input id="last_name" type="text" className="validate" required/>
                        <label htmlFor="last_name">Last Name</label>
                    </div>
                </div>
                <div className="row">
                    <div className="col s12">
                        <input id="username" type="text" className="validate" required/>
                        <label htmlFor="username">Username</label>
                    </div>
                </div>
                <div className="row">
                    <div className="col s12">
                        <input id="email" type="email" className="validate" required/>
                        <label htmlFor="email">Email</label>
                    </div>
                </div>
                <div className="row">
                    <div className="col s4">
                        <input id="city" type="text" className="validate" required/>
                        <label htmlFor="city">City</label>
                    </div>
                    <div className="col s4">
                        <input id="zipcode" type="text" className="validate" required/>
                        <label htmlFor="zipcode">Zip Code</label>
                    </div>
                    <div className="col s4">
                        <input id="state" type="text" className="validate" required/>
                        <label htmlFor="state">State</label>
                    </div>
                </div>
                <div className="row">
                    <div className="col s12">
                        <input id="address" type="text" className="validate" required/>
                        <label htmlFor="address">Address</label>
                    </div>
                </div>
                <div className="row">
                    <div className="col s12">
                        <input id="password" type="password" className="validate" required/>
                        <label htmlFor="password">Password</label>
                    </div>
                </div>
                <div className="row">
                    <div className="col s12">
                        <input id="confirm_password" type="password" className="validate" required/>
                        <label htmlFor="confirm_password">Re-Enter Password</label>
                    </div>
                </div>
                <div className="center-align">
                    <button className="btn waves-effect waves-light" type="submit" name="action">Signup</button>
                </div>
                <Link to="/login">Already have an account? Login</Link>
            </form>
        </div>
    )
};

export default Register;
