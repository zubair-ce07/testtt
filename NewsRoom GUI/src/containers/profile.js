import React, { Component } from 'react';
import { Field, reduxForm } from 'redux-form';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import { loginUser } from '../actions'

class Profile extends Component {
    renderField(field) {
        const { meta: { touched, error } } = field;
        const className = `form-group ${touched && error ? 'has-error' : ''}`;
        return (
            <div className={className}>
                <label>{ field.label }</label>
                <input 
                    className="form-control" 
                    type={ field.type } 
                    { ...field.input } 
                />
                <div className="text-danger">
                    { touched ? error : '' }
                </div>
            </div>
        );
    }

    onSubmit(values) {
        this.props.loginUser(values).then(() => {
            this.props.history.push('/news');
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
                <button type="submit" className="btn btn-primary">Submit</button>
                <br />
                <div className="center-content">
                    <Link to="/signup">Don't have an account yet</Link>
                </div>
            </form>
        );
    }
}

function validate(values) {
    const errors = {};

    if (!values.email) {
        errors.email = "Enter a email address!";
    }
    if (values.email &&  !/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i.test(values.email)) {
       errors.email = "Enter a valid email address!";
    }
    if (!values.password) {
        errors.password = "Enter password!";
    }
    return errors;
}

function mapStateToProps({ user }){
    return { user }
}

export default reduxForm({
    validate,
    form: 'LoginForm'
})(
    connect(mapStateToProps, { loginUser })(Login)
);