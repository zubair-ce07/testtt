import React from 'react'


const Register = () => {
    return (
        <div className="container">
            <form>
                <h4 className="center">Register!</h4>
                <div class="row">
                    <div class="col s6">
                        <input id="first_name" type="text" className="validate"/>
                        <label for="first_name">First Name</label>
                    </div>
                    <div class="col s6">
                        <input id="last_name" type="text" className="validate"/>
                        <label for="last_name">Last Name</label>
                    </div>
                </div>
                <div class="row">
                    <div class="col s12">
                        <input id="username" type="text" className="validate"/>
                        <label for="username">Username</label>
                    </div>
                </div>
                <div class="row">
                    <div class="col s12">
                        <input id="email" type="email" className="validate"/>
                        <label for="email">Email</label>
                    </div>
                </div>
                <div class="row">
                    <div class="col s12">
                        <input id="password" type="password" className="validate"/>
                        <label for="password">Password</label>
                    </div>
                </div>
                <div class="row">
                    <div class="col s12">
                        <input id="confirm_password" type="password" className="validate"/>
                        <label for="confirm_password">Re-Enter Password</label>
                    </div>
                </div>
                <div className="center-align">
                    <button class="btn waves-effect waves-light" type="submit" name="action">Signup</button>                </div>
            </form>
        </div>
    )
};

export default Register;
