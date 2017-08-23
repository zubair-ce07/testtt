import React from 'react';
import { connect } from 'react-redux';
import { browserHistory } from 'react-router';
import { reduxForm, Field } from 'redux-form';

import { signupTrainee } from '../actions/trainee_signup';


class TraineeSignup extends React.Component
{
    componentWillMount()
    {
        if(localStorage.getItem("token"))
        {
            browserHistory.push('/profile');
        }
    }

    inputField(field)
    {
        return (
            <div className="form-group">
                <input
                    className="form-control"
                    type={ field.type }
                    { ...field.input }
                />
                <p className="error">{ field.meta.touched ? field.meta.error : ''}</p>
            </div>
        );
    }

    imageField(field)
    {
        return(
            <div>
                <input type="file" name="pic" accept="image/*" { ...field.input }/>
                <p className="error">{ field.meta.touched ? field.meta.error : ''}</p>
            </div>
        )
    }

    submit(values)
    {
        this.props.signupTrainee(values)
            .then((response) => {
                browserHistory.push("/");
            })
            .catch((error) => {
                console.log(error);
                document.getElementById("error-msg").style.display = 'block';
            })
    }

    render()
    {
        const { handleSubmit }  = this.props;
        return (
            <div className="container col-md-4 col-md-offset-4">
                <form onSubmit={ handleSubmit(this.submit.bind(this)) }>
                    <h3>Trainer Signup</h3>
                    <div id="error-msg" hidden className="alert alert-danger">
                        <strong>Username / Password</strong>{' '}is Incorrect
                    </div>

                    <div className="form-group ">
                        <label>Username</label>
                        <Field type="text" name="username" component={ this.inputField }
                               className="form-control" />
                    </div>

                    <div className="form-group">
                        <label>First Name</label>
                        <Field type="text" name="first_name" component={ this.inputField }
                               className="form-control" />
                    </div>

                    <div className="form-group">
                        <label>Last Name</label>
                        <Field type="text" name="last_name" component={ this.inputField }
                               className="form-control" />
                    </div>

                    <div className="form-group">
                        <label>Password</label>
                        <Field type="password" name="password" component={ this.inputField }
                               className="form-control" />
                    </div>

                    <div className="form-group">
                        <label>Picture</label>
                        <Field type="file" name="picture" component={ this.imageField }
                               className="form-control" />
                    </div>

                    <button type="submit" className="btn btn-primary btn-block">Submit</button>
                </form>
            </div>
        )
    }
}

function validate(values)
{
    let errors = {};
    if(!values.username)
    {
        errors.username = 'Username Required';
    }
    if(!values.first_name)
    {
        errors.first_name = 'First Name Required';
    }
    if(!values.last_name)
    {
        errors.last_name = 'Last Name Required';
    }
    if(!values.password)
    {
        errors.password = 'Password Required';
    }

    return errors;
}

export default reduxForm({
    form: 'TraineeSignupForm',
    validate,
})(connect(null, { signupTrainee })(TraineeSignup));