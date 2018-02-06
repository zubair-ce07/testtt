import React from 'react';
import PropTypes from 'prop-types'

export default class LoginForm extends React.Component {
    static propTypes = {
          onSubmit: PropTypes.func.isRequired,
          onChange: PropTypes.func.isRequired,
          errors: PropTypes.object.isRequired,
          user: PropTypes.object.isRequired
    };
    constructor(props) {
    super(props);
          this.onSubmit = props.onSubmit;
          this.onChange = props.onChange;
          this.errors = props.errors;
          this.user = props.user;
    }

    render() {
        return (
             <form onSubmit={this.onSubmit}>
                <div className="section-title">
                    <h3>LogIn to your Account</h3>
                </div>
                <div className="textbox-wrap">
                    <div className="input-group">
                        <span className="input-group-addon "><i className="fa fa-user"></i></span>
                        <input name="name" type="text" required="required" className="form-control" placeholder="Username"
                         onChange={this.onChange} value={this.user.name}/>
                    </div>
                </div>
                <div className="textbox-wrap">
                    <div className="input-group">
                        <span className="input-group-addon "><i className="fa fa-key"></i></span>
                        <input type="password" name="password" required="required" className="form-control " placeholder="Password"
                           onChange={this.onChange} value={this.user.password}/>
                    </div>
                </div>
                <div className="login-check">
                    <label className="checkbox1"><input type="checkbox" name="checkbox" checked=""/><i> </i>Sign Up for Newsletter</label>
                </div>
                <div className="login-para">
                   <p><a href="#"> Forgot Password? </a></p>
                </div>
                <div className="clearfix"> </div>
                <div className="login-btn">
                    <input type="submit" value="Log in"/>
                </div>
             </form>
        );
    }
}

