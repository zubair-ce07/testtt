import React, { Component } from 'react';
import { Field, reduxForm } from 'redux-form';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import { signupUser } from '../actions'


class Signup extends Component {
    renderField(field) {
        const { meta: { touched, error } } = field;
        const className = `form-group ${touched && error ? 'has-error has-feedback' : touched ? 'has-success has-feedback':''}`;
        return (
            <div className={className}>
                <label className="control-label">{ field.label }</label>
                <input 
                    className="form-control"
                    aria-describedby={field.name} 
                    type={ field.type } 
                    { ...field.input } 
                />
                <span 
                    className={`glyphicon ${touched && error ? 'glyphicon-remove' : 
                                            touched ? 'glyphicon-ok':''} form-control-feedback`} 
                    aria-hidden="true">
                </span>
                <span 
                    id={ field.name } 
                    className="sr-only"
                >
                    {touched && error ? '(error)' : touched ? '(success)':''}
                </span>
                <div className="text-danger">
                    { touched ? error : '' }
                </div>
            </div>
        );
    }

    onSubmit(values) {
        this.props.signupUser(values).then(() => {
            this.props.history.push('/login');
        });
    }

    render() {
        const handleSubmit = this.props.handleSubmit;
        return (
            <form onSubmit={ handleSubmit(this.onSubmit.bind(this)) }>
                <Field 
                    label="Email" 
                    name="email" 
                    type="email"
                    component={ this.renderField } 
                />
                <Field
                    label="Password"
                    name="password"
                    type="password"
                    component={ this.renderField }
                />
                <Field
                    label="Confirm Password"
                    name="password2"
                    type="password"
                    component={ this.renderField }
                />
                <Field
                    label="First Name"
                    name="first_name"
                    type="text"
                    component={ this.renderField }
                />
                <Field
                    label="Last Name"
                    name="last_name"
                    type="text"
                    component={ this.renderField }
                />
                <button type="submit" className="btn btn-primary">Signup</button>
            </form>
        );
    }
}

function validate(values) {
    const errors = {};

    if (!values.email) {
        errors.email = "Enter a email address!";
    }
    if (!values.password) {
        errors.password = "Enter password!";
    }
    if (!values.password2) {
        errors.password2 = "Enter password!";
    }
    if (values.password2 && values.password != values.password2) {
        errors.password2 = "Password doesn't match";
    }
    if (!values.first_name){
        errors.first_name = "Enter your First Name";
    }
    if (!values.last_name){
        errors.last_name = "Enter your Last Name";
    }
    return errors;
}

export default reduxForm({
    validate,
    form: 'SignupForm'
})(
    connect(null, { signupUser })(Signup)
);