import _ from 'lodash';
import Moment from 'moment'
import {connect} from 'react-redux';
import React, {Component} from 'react';
import {Link} from 'react-router-dom';
import {Field, reduxForm} from 'redux-form';
import DateTimePicker from 'react-widgets/lib/DateTimePicker'
import {UncontrolledAlert} from 'reactstrap';
import momentLocalizer from 'react-widgets-moment'

import 'react-widgets/dist/css/react-widgets.css'

import {signupUser} from '../../actions/user_actions';


Moment.locale('en');
momentLocalizer();

class Signup extends Component {
    constructor(props) {
        super(props);

        this.state = {
            errors: null
        };
    }

    onSubmit(values) {
        this.setState({'errors': null});
        this.props.signupUser(values).then(
            (res) => {
                this.props.history.push('/');
            },
            (err) => {
                this.setState({'errors': err.response.data});
            });
    }

    renderErrors() {
        return _.map(this.state.errors, (value, key) => {
            return <UncontrolledAlert color="warning" key={key}>{value}</UncontrolledAlert>
        });
    }

    render() {
        const handleSubmit = this.props.handleSubmit;
        return (
            <div className="mx-auto sign-card">
                {this.renderErrors()}
                <form onSubmit={handleSubmit(this.onSubmit.bind(this))}>
                    <div className="row">
                        <div className="col-md-6">
                            <Field label="First Name" name="first_name" type="text" component={renderField}/>
                        </div>
                        <div className="col-md-6">
                            <Field label="Last Name" name="last_name" type="text" component={renderField}/>
                        </div>
                    </div>
                    <div className="row">
                        <div className="col-md-12">
                            <Field label="Email" name="email" type="email" component={renderField}/>
                        </div>
                    </div>
                    <div className="row">
                        <div className="col-md-6">
                            <Field label="Password" name="password" type="password" component={renderField}/>
                        </div>
                        <div className="col-md-6">
                            <Field label="Confirm Password" name="password2" type="password" component={renderField}/>
                        </div>
                    </div>
                    <div className="row">
                        <div className="col-md-6">
                            <Field label="Profile Photo" name="photo" type="file" component={renderField}/>
                        </div>
                        <div className="col-md-6">
                            <Field label="Date Of Birth" name="date_of_birth" type="date" component={renderField}/>
                        </div>
                    </div>
                    <div className="row">
                            <button type="submit" className="btn btn-secondary signup-btn mx-auto">Signup</button><br/>
                    </div>
                    <div className="row pad6y w-55 mx-auto">Ha! Already got an account?
                        <Link to="/login/"> get there</Link>
                    </div>
                </form>
            </div>
        );
    }
}

function validate(values) {
    const errors = {};
    if (!values.first_name) {
        errors.first_name = "Enter your First Name";
    }
    if (!values.last_name) {
        errors.last_name = "Enter your Last Name";
    }
    if (!values.email) {
        errors.email = "Enter a email address!";
    }
    if (!values.password) {
        errors.password = "Enter password!";
    }
    if (!values.password2) {
        errors.password2 = "Enter password!";
    }
    if (values.password2 && values.password !== values.password2) {
        errors.password2 = "Password doesn't match";
    }
    if (!values.photo || !values.photo[0]) {
        errors.photo = "Add a profile Photo";
    }
    if (!values.date_of_birth) {
        errors.date_of_birth = "Add your date of birth";
    }
    return errors;
}

function renderField(field) {
    const {meta: {touched, error}} = field;
    const className = `form-group ${touched && error ? 'has-error has-feedback' : touched ? 'has-success has-feedback' : ''}`;
    let input = null;
    if (field.type === "file")
        input = <input className="form-control" type={field.type} accept="image/*" {...field.input} value={undefined}/>;
    else if (field.type === "date")
        input =
            <DateTimePicker onChange={field.input.onChange} format="DD MMMM YYYY" className="form-control date-picker"
                            time={false} value={!field.input.value ? null : new Date(field.input.value)}/>;
    else
        input = <input className="form-control" type={field.type} {...field.input} />;
    return (
        <div className={className}>
            <label className="control-label">{field.label}</label>
            {input}
            <div className="text-warning">
                {touched ? error : ''}
            </div>
        </div>
    );
}

export default reduxForm({
    validate,
    form: 'SignupForm'
})(
    connect(null, {signupUser})(Signup)
);
