import React, { Component } from 'react';
import { Field, reduxForm } from 'redux-form';
import { updateUserProfile } from '../actions';
import { connect } from 'react-redux';
import { reactLocalStorage } from 'reactjs-localstorage';


class ProfileForm extends Component {
    constructor(props){
        super(props);
        this.state = {read_only: true};
        this.renderField = this.renderField.bind(this);

    }

    renderField(field) {
        return (
            <div className="form-group">
                <label className="control-label">{ field.label }</label>
                <input 
                    className="form-control"
                    aria-describedby={field.name} 
                    type={ field.type }    
                    { ...field.input }
                    readOnly={field.read_value}
                />       
            </div>
        );
    }

    onEdit() {
        this.setState({read_only: false});
    }

    onSubmit(values){
        const token = reactLocalStorage.get('token', "");
        this.props.updateUserProfile(token, values);
        this.setState({read_only: true});
    }

    toggleDisplay(display_property){
        return display_property ? 'block': 'none';
    }

    render() {
        const handleSubmit = this.props.handleSubmit;
        let updateButton = this.toggleDisplay(this.state.read_only);
        let editButton = this.toggleDisplay(!this.state.read_only);;
        return (
            <div>
            <form onSubmit={ handleSubmit(this.onSubmit.bind(this))}>
                <Field 
                    label="Email" 
                    name="email" 
                    type="email"
                    read_value="true"
                    component={ this.renderField }
                />
                <Field
                    label="First Name"
                    name="first_name"
                    type="text"
                    read_value={this.state.read_only}
                    component={ this.renderField }
                />
                <Field
                    label="Last Name"
                    name="last_name"
                    type="text"
                    read_value={this.state.read_only}
                    component={ this.renderField }
                />
                <button type="submit" className="btn btn-primary" style={{display:updateButton}}>Update</button>
            </form>
            <button onClick={this.onEdit.bind(this)} className="btn btn-primary" style={{display:editButton}}>Edit</button>
            </div>
        );
    }
}

function validate(values) {
    const errors = {};

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
    form: 'ProfileForm'
})(
    connect(null, { updateUserProfile })(ProfileForm)
);