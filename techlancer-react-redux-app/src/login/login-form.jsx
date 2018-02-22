import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import React from 'react';

import PropTypes from 'prop-types'

import * as Actions from './actions.js'

class LoginForm extends React.Component {
    static propTypes =  {
        actions: PropTypes.object,
        user: PropTypes.string
    };
    constructor(props) {
    console.log("Form", "Login");
        super(props);
        // set the initial component state
        this.state = {
        errors: {},
        user: {
            name: '	',
            password: ''
        }
    };  

    this.processForm = this.processForm.bind(this);
    this.changeUser = this.changeUser.bind(this);
}
changeUser(event) {
    const field = event.target.name;
    const user = this.state.user;
    user[field] = event.target.value;

    this.setState({
        user
    }); 
}

/**
 * Process the form.
 *
 * @param {object} event - the JavaScript event object
 */
processForm(event) {
    // prevent default action. in this case, action is the form submission event
    event.preventDefault();

    console.log('name:', this.state.user.name);
    console.log('email:', this.state.user.email);
    console.log('password:', this.state.user.password);
    this.props.actions.requestAuthorization(this.state.user);
    
}

    render() {
        return (
            <form onSubmit={this.processForm}>
                <div className="section-title">
                    <h3>LogIn to your Account</h3>
                </div>
                <div className="textbox-wrap">
                    <div className="input-group">
                        <span className="input-group-addon "><i className="fa fa-user"></i></span>
                        <input name="name" type="text" required="required" className="form-control" placeholder="Username"
                         onChange={this.changeUser} value={this.state.user.name}/>
                    </div>
                </div>
                <div className="textbox-wrap">
                    <div className="input-group">
                        <span className="input-group-addon "><i className="fa fa-key"></i></span>
                        <input type="password" name="password" required="required" className="form-control " placeholder="Password"
                           onChange={this.changeUser} value={this.state.user.password}/>
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

function mapStateToProps(state) {
    return {
        user: state.login_reducer.token
    };
}

function mapDispatchToProps(dispatch) {
    return {
        actions: bindActionCreators(Actions, dispatch)
    };
}
export default connect(
    mapStateToProps,
    mapDispatchToProps
)(LoginForm);

