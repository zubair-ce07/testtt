import React, {Component} from "react";
import {browserHistory} from "react-router";
import {connect} from "react-redux";
import {getUserProfile, updateProfile} from "../actions";
import {Field, reduxForm} from "redux-form";

class EditProfile extends Component {
    componentWillMount() {
        if (localStorage.getItem('token')) {
            this.props.getUserProfile(this.props.params.id, localStorage.getItem('token'));
        } else {
            browserHistory.push('/');
        };
    };
    inputField(field) {
        return (
            <div>
                <span className="alert">{ field.meta.touched ? field.meta.error : ''}</span>
                <input
                    className="form-control"
                    type={ field.type }
                    { ...field.input }/>
            </div>
        );
    };
    imageField(field) {
        return (
            <div>
                <span className="error">{ field.meta.touched ? field.meta.error : ''}</span>
                <input type="file" name="pic" accept="image/*" { ...field.input }/>
            </div>
        );
    };
    submit(values) {
        let formData = new FormData();
        formData.append('id', this.props.initialValues.id);
        formData.append('password', this.props.initialValues.password);
        formData.append('first_name', values.first_name);
        formData.append('last_name', values.last_name);
        formData.append('email', values.email);
        formData.append('username', values.username);
        formData.append('tags', values.tags);
        if (values.image[0].name) {
            formData.append('image', values.image[0]);
        };
        this.props.updateProfile(formData, this.props.initialValues.id, localStorage.getItem('token')).then(() => {
            browserHistory.push('/home');
        });
    };
    render() {
        const {handleSubmit} = this.props;
        return (
            <div className="col-md-7 col-md-offset-2">
                <form onSubmit={ handleSubmit(this.submit.bind(this)) }>
                    <center><h2><b>Edit Your Profile</b></h2></center>
                    <br/>
                    <div id="error-msg" hidden className="alert alert-danger">
                        <strong>Username / Password</strong>{' '}is Incorrect
                    </div>
                    <div className="form-group">
                        <label>First Name</label>
                        <Field type="text" name="first_name" component={ this.inputField }
                               className="form-control"/>
                    </div>
                    <div className="form-group">
                        <label>Last Name</label>
                        <Field type="text" name="last_name" component={ this.inputField }
                               className="form-control"/>
                    </div>
                    <div className="form-group ">
                        <label>Username</label>
                        <Field type="text" name="username" component={ this.inputField }
                               className="form-control"/>
                    </div>
                    <div className="form-group ">
                        <label>Email</label>
                        <Field type="email" name="email" component={ this.inputField }
                               className="form-control"/>
                    </div>
                    <div className="form-group">
                        <label>Image</label>
                        <Field type="file" name="image" component={ this.imageField }
                               className="form-control"/>
                    </div>
                    <button type="submit" className="btn btn-primary btn-block">Update</button>
                </form>
            </div>
        );
    };
};
function validate(values) {
    let errors = {};
    if (!values.username) {
        errors.username = 'Username Required';
    }; if (!values.first_name) {
        errors.first_name = 'First Name Required';
    }; if (!values.email) {
        errors.email = 'Email Required';
    }
    return errors;
};
EditProfile = reduxForm({
    form: 'EditProfileForm'
})(EditProfile)
EditProfile = connect(
    state => ({
        initialValues: state.user,
        validate
    }),
    {
        getUserProfile: getUserProfile,
        updateProfile: updateProfile
    }
)(EditProfile)
export default EditProfile;
