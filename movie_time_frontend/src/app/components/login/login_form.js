import React, {Component} from 'react';
import {Field, reduxForm} from 'redux-form';
import {connect} from 'react-redux';
import {UncontrolledAlert} from 'reactstrap';
import {Link} from 'react-router-dom';

import {login} from '../../actions/auth_actions';


class LoginForm extends Component {
    constructor(props) {
        super(props);

        this.state = {
            error: null
        };
    }

    onSubmit(values) {
        this.setState({'error': null});
        this.props.login(values).then(
            (res) => {
                this.props.history.push('/')
            },
            (err) => {
                this.setState({'error': err.response.data.detail});
                console.log('Failed')
            }
        );
    }

    render() {
        const handleSubmit = this.props.handleSubmit;
        return (
            <div className="mx-auto sign-card w-25">

                {this.state.error? (<UncontrolledAlert color="warning">{this.state.error}</UncontrolledAlert>) : ''}
            <form onSubmit={handleSubmit(this.onSubmit.bind(this))}>
                <Field label="Email" name="email" type="email" component={renderField}/>
                <Field label="Password" name="password" type="password" component={renderField}/>
                <div className="row">
                    <button type="submit" className="btn btn-secondary signup-btn mx-auto">Login</button><br/>
                </div>
                <div className="row pad6y w-90 mx-auto">what! You got no account?
                    <Link to="/signup/"> create it already</Link>
                </div>
            </form>
            </div>
        );
    }
}

function renderField(field) {
    const {meta: {touched, error}} = field;
    const className = `form-group ${touched && error ? 'has-error' : ''}`;
    return (
        <div className={className}>
            <label>{field.label}</label>
            <input className="form-control" type={field.type} {...field.input} />
            <div className="text-danger">
                {touched ? error : ''}
            </div>
        </div>
    );
}

function validate(values) {
    const errors = {};
    if (!values.email) {
        errors.email = "Enter a email address!";
    }
    if (values.email && !/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i.test(values.email)) {
        errors.email = "Enter a valid email address!";
    }
    if (!values.password) {
        errors.password = "Enter password!";
    }
    return errors;
}

export default reduxForm({
    validate,
    form: 'LoginForm'
})(connect(null, {login})(LoginForm));
