import React from 'react'


const Login = () => {
    return (
        <div className="container">
            <form>
                <h4 className="center">Login</h4>
                <input id="username" type="text" className="validate"/>
                <label for="username">Username</label>
                <br/>
                <br/>
                <input id="password" type="password" className="validate"/>
                <label for="password">Password</label>
                <div className="center-align">
                    <button class="btn waves-effect waves-light" type="submit" name="action">Login</button>                </div>
            </form>
        </div>
    )
};

export default Login;
