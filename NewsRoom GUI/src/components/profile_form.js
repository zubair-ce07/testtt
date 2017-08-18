import React, { Component } from 'react';
import { Field, reduxForm } from 'redux-form';
import _ from 'lodash';


class ProfileForm extends Component {
    constructor(props){
        super(props);
        this.state = {read_only: true};
        this.renderField = this.renderField.bind(this);

    }

    renderField(field) {
        
        // const readonly = 'readonly'
        console.log("TOuched", field);
        /*value={field.read_value ? field.data : field.input.value }*/
         
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

    }

    toggleDisplay(display_property){
        return display_property ? 'block': 'none';
    }

    render() {
        const handleSubmit = this.props.handleSubmit;
        console.log("Study display property", !this.state.read_only);
        let dis = this.toggleDisplay(this.state.read_only);
        let dis1 = this.toggleDisplay(!this.state.read_only);;
        console.log("P1: ", dis);
        console.log("P2: ", dis1);
        return (
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
                <button onClick={this.onEdit.bind(this)} className="btn btn-primary" style={{display:dis}}>Edit</button>
                <button type="submit" className="btn btn-primary" style={{display:dis1}}>Update</button>
            </form>
        );
    }
}

export default reduxForm({
    form: 'ProfileForm',
})(ProfileForm);