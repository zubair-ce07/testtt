import React from 'react';
import TextField from '@material-ui/core/TextField';
import MenuItem from '@material-ui/core/MenuItem';
import Select from '@material-ui/core/Select';
import PropTypes from 'prop-types';

const textFieldStyle = {
    width: '100%'
};

export const  renderField = ({ input,label, type,meta: { touched, error },...custom}) => (
    <TextField
        label={touched && error!==undefined?(error):(label)}
        style={textFieldStyle}
        error={touched && error !== undefined}
        margin="normal"
        variant="outlined"
        type={type}
        {...input}
        {...custom}
    />
);

export const  renderSelectField = ({ input,...custom}) => (
    <Select
        {...input}
        {...custom}
    >
        <MenuItem value={'15'}>15 minutes</MenuItem>
        <MenuItem value={'30'}>30 minutes</MenuItem>
        <MenuItem value={'45'}>45 minutes</MenuItem>
        <MenuItem value={'60'}>60 minutes</MenuItem>
    </Select>
);
renderSelectField.propTypes = {
    input: PropTypes.object.isRequired,
};

renderField.propTypes = {
    input: PropTypes.object.isRequired,
    label: PropTypes.string.isRequired,
    type : PropTypes.string.isRequired,
    meta: PropTypes.object.isRequired

};


export const validate = values => {
    const errors = {};
    const requiredFields = [
        'username',
        'password',
        'password1',
        'password2',
        'email',
        'first_name',
        'last_name',
        'phone_no',
        'address',
        'start_date',
        'end_date',
        'start_time',
        'slot_duration',
        'number_of_slots'
    ];
    requiredFields.forEach(field => {
        if (!values[field]) {
            errors[field] = 'Required';
        }
    });
    if (
        values.email &&
        !/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i.test(values.email)
    ) {
        errors.email = 'Invalid email address';
    }
    if(values.password1 !== values.password2){
        errors.password2 = 'Password does not match';
    }
    if(values.start_date > values.end_date){
        errors.end_date = 'End date should be greater than start date';
    }
    return errors;
};