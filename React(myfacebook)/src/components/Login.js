import React from 'react';

import { Field, reduxForm } from 'redux-form';
import { browserHistory} from 'react-router';
import { connect } from 'react-redux';

import { LoginUser } from "../actions/LoginUser";


class Login extends React.Component
{
    componentWillMount()
    {
        if(localStorage.getItem("token"))
        {
            browserHistory.push('/news');
        }
    }

    inputField(props)
    {
        return (
            <div className="form-group">
                <input className="form-control"
                       placeholder={props.input.name}
                       type={props.type}
                       {...props.input}/>
                <p className="alert-warning">{ props.meta.touched ? props.meta.error : ''}</p>
            </div>
        );
    }

    submit(values)
    {
        this.props.LoginUser(values)
        .then((response) => {
            localStorage.setItem("token", response.payload.data.token);
            browserHistory.push("/news");
        })
        .catch((error) => {
            console.log(error);
            document.getElementById("error-msg").style.display = 'block';
        })
    }

    render()
    {

        const { handleSubmit } = this.props;
        return (
            <div className="container col-md-4 col-md-offset-4">
                <form onSubmit={ handleSubmit(this.submit.bind(this)) }>
                    <h3>SignIn</h3>
                    <div id="error-msg" hidden className="alert alert-danger">
                        <strong>Username / Password </strong>is Incorrect
                    </div>
                    <div className="form-group ">
                        <Field type="text" name="username" component={ this.inputField }
                               className="form-control" />
                    </div>

                    <div className="form-group">
                        <Field type="password" name="password" component={ this.inputField }
                               className="form-control" />
                    </div>

                    <button type="submit" className="btn btn-primary btn-block">SignIn</button>
                </form>
            </div>
        );
    }
}
function validate(values)
{
    let errors = {};

    if(!values.username)
    {
        errors.username = 'Username Required';
    }

    if(!values.password)
    {
        errors.password = 'Password Required';
    }

    return errors;
}

export default reduxForm({
    validate,
    form: 'LoginForm',
})(connect(null, { LoginUser })(Login));