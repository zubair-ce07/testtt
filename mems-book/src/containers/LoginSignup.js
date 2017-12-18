import React, {Component} from "react";
import {connect} from "react-redux";
import {bindActionCreators} from "redux";
import {browserHistory} from "react-router";
import {Field, reduxForm} from "redux-form";
import {Login, LoginClick, signup, SignUpClick} from "../actions";

let tab = '';
class LoginSignup extends Component {
    componentWillMount() {
        if (localStorage.getItem('token')) {
            browserHistory.push('/home');
        };
    };
    componentWillUpdate() {
        if (localStorage.getItem('token')) {
            browserHistory.push('/home');
        };
    };
    isError() {
        if (this.props.token === false) {
            return (
                <div className="form-group">
                    <div className="row">
                        <div className="col-sm-8 col-sm-offset-3">
                            <strong><span className="alert"> Email or password is not correct </span></strong>
                        </div>
                    </div>
                </div>
            );
        };
        return '';
    };
    inputField(field) {
        return (
            <div>
                <span className="alert">{ field.meta.touched ? field.meta.error : ''}</span>
                <input
                    className="form-control"
                    type={ field.type }
                    placeholder={field.placeholder}
                    { ...field.input }/>
            </div>
        );
    };
    submitLogin(values) {
        let credentials = {email: values.email, password: values.password};
        this.props.Login(credentials);
    };
    submitSigup(values) {
        let data = {
            first_name: values.first_name,
            last_name: values.last_name,
            email: values.signup_email,
            password: values.signup_password,
            username: values.username
        };
        this.props.signup(data).then(() => {
            browserHistory.push('/home')
        });
    };
    render() {
        tab = this.props.tab;
        const {handleSubmit} = this.props;
        return (
            <div className="container">
                <br/><br/>
                <div className="row">
                    <div className="col-md-6 col-md-offset-3">
                        <div className="panel panel-login">
                            <div className="panel-heading">
                                <div className="row">
                                    <div className="col-xs-6">
                                        <a href="" className={this.props.tab === 'login' ? 'active' : ''}
                                           id="login-form-link"
                                           onClick={e => {
                                               e.preventDefault();
                                               this.props.LoginClick();
                                           }}>
                                            Login
                                        </a>
                                    </div>
                                    <div className="col-xs-6">
                                        <a href="" className={this.props.tab === 'signup' ? 'active' : ''}
                                           id="register-form-link" onClick={e => {
                                            e.preventDefault();
                                            this.props.SignUpClick();
                                        }}>Register</a>
                                    </div>
                                </div><hr/>
                            </div>
                            <div className="panel-body">
                                <div className="row">
                                    <div className="col-lg-12">
                                        <form id="login-form"
                                              className={this.props.tab === 'login' ? 'active-form' : 'unactive-form'}
                                              onSubmit={ handleSubmit(this.submitLogin.bind(this)) }>
                                            {this.isError()}
                                            <div className="form-group">
                                                <div className="row">
                                                    <div className="col-md-12">
                                                        <Field type="text" name="email" placeholder="email"
                                                               component={this.inputField}
                                                        />
                                                    </div>
                                                </div>
                                            </div>
                                            <div className="form-group">
                                                <div className="row">
                                                    <div className="col-md-12">
                                                        <Field type="password" placeholder="password" name="password"
                                                               component={this.inputField}
                                                        />
                                                    </div>
                                                </div>
                                            </div>
                                            <div className="form-group">
                                                <div className="row">
                                                    <div className="col-sm-6 col-sm-offset-3">
                                                        <input type="submit" name="login-submit" id="login-submit"
                                                               tabIndex="4" className="form-control btn btn-login"
                                                               value="Log In"/>
                                                    </div>
                                                </div>
                                            </div>
                                        </form>
                                        <form id="register-form" action="/signup" method="post"
                                              encType="multipart/form-data"
                                              className={this.props.tab === 'signup' ? 'active-form' : 'unactive-form' }
                                              onSubmit={ handleSubmit(this.submitSigup.bind(this)) }>
                                            <div className="form-group">
                                                <div className="row">
                                                    <div className="col-md-12">
                                                        <Field type="text" name="first_name" placeholder="First Name"
                                                               component={this.inputField}/>
                                                    </div>
                                                </div>
                                            </div>
                                            <div className="form-group">
                                                <div className="row">
                                                    <div className="col-md-12">
                                                        <Field type="text" name="last_name" placeholder="Lat Name"
                                                               component={this.inputField}/>
                                                    </div>
                                                </div>
                                            </div>
                                            <div className="form-group">
                                                <div className="row">
                                                    <div className="col-md-12">
                                                        <Field type="text" name="username" placeholder="username"
                                                               component={this.inputField}/>
                                                    </div>
                                                </div>
                                            </div>
                                            <div className="form-group">
                                                <div className="row">
                                                    <div className="col-md-12">
                                                        <Field type="text" name="signup_email" placeholder="email"
                                                               component={this.inputField}/>
                                                    </div>
                                                </div>
                                            </div>
                                            <div className="form-group">
                                                <div className="row">
                                                    <div className="col-md-12">
                                                        <Field type="password" name="signup_password"
                                                               placeholder="password" component={this.inputField}/>
                                                    </div>
                                                </div>
                                            </div>
                                            <div className="form-group">
                                                <div className="row">
                                                    <div className="col-sm-6 col-sm-offset-3">
                                                        <input type="submit" name="register-submit" id="register-submit"
                                                               tabIndex="4" className="form-control btn btn-register"
                                                               value="Register Now"/>
                                                    </div>
                                                </div>
                                            </div>
                                        </form>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );
    };
};
function validateEmail(email) {
    var emailRegex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return emailRegex.test(email);
};
function validate(values) {
    let errors = {};
    if (tab === 'login') {
        if (!validateEmail(values.email)) {
            errors.email = ' Email is not correct';
        }; if (!(values.password && values.password.length >= 8)) {
            errors.password = ' Password is not correct';
        };
    } else {
        if (!values.first_name) {
            errors.first_name = " First Name is required";
        }; if (!validateEmail(values.signup_email)) {
            errors.signup_email = " Email is not correct";
        }; if (!values.username) {
            errors.username = " Username is required";
        }; if (!(values.signup_password && values.signup_password.length >= 8)) {
            errors.signup_password = " Minimum length required is 8";
        };
    };
    return errors;
};
function mapStateToProps(state) {
    return {
        tab: state.tab,
        token: state.token,
        user: state.user
    };
};
function mapDispatchToProps(dispatch) {
    return bindActionCreators({
            LoginClick: LoginClick,
            SignUpClick: SignUpClick,
            Login: Login,
            signup: signup
        }, dispatch);
};
export default reduxForm({
    form: 'LoginSignupForm',
    validate: validate
})(connect(mapStateToProps, mapDispatchToProps)(LoginSignup));
