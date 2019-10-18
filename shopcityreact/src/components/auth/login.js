import React from 'react';
import { Link } from 'react-router-dom';


const Login = () => {
    return (
        <div className="container">
            <form>
                <h4 className="center">Login</h4>
                <input id="username" type="text" className="validate" required/>
                <label htmlFor="username">Username</label>
                <br/>
                <br/>
                <input id="password" type="password" className="validate" required/>
                <label htmlFor="password">Password</label>
                <div className="center-align">
                    <button className="btn waves-effect waves-light" type="submit" name="action">Login</button>
                </div>
                <Link to="/register">Dont't have an account? Signup</Link>
            </form>
        </div>
    )
};

export default Login;
