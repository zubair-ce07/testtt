import React from 'react'
import { Field, reduxForm } from 'redux-form'
import {connect} from 'react-redux'

const required = value => value ? undefined : 'Required'
const maxLength = max => value =>
    value && value.length > max ? `Must be ${max} characters or less` : undefined
const maxLength15 = maxLength(15)
const number = value => value && isNaN(Number(value)) ? 'Must be a number' : undefined
const minValue = min => value =>
    value && value < min ? `Must be at least ${min}` : undefined
const minValue18 = minValue(1)
const email = value =>
    value && !/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i.test(value) ?
        'Invalid email address' : undefined
const tooOld = value =>
    value && value > 65 ? 'You might be too old for this' : undefined
const aol = value =>
    value && /.+@aol\.com/.test(value) ?
        'Really? You still use AOL for your email?' : undefined

const renderField = ({ input, label, type, meta: { touched, error, warning } }) => (
    <div>
        <label>{label}</label>
        <div>
            <input {...input} placeholder={label} type={type}/>
            {touched && ((error && <span>{error}</span>) || (warning && <span>{warning}</span>))}
        </div>
    </div>
)

let FieldLevelValidationForm = props => {
    const {handleSubmit, load, pristine, reset, submitting} = props
    return (
        <form onSubmit={handleSubmit}>

            <div>
                <label>Name</label>
                <div>
                    <Field name="author" type="text"
                           component={renderField}
                           validate={[ required, maxLength15 ]}
                    />
                </div>
            </div>

            <div>
                <label>Comment</label>
                <div>
                    <Field name="body" type="textarea"  component={renderField}  />
                </div>
            </div>
            <div>
                <button type="submit" disabled={pristine || submitting}>Submit</button>
                <button type="button" disabled={pristine || submitting} onClick={reset}>
                    Undo Changes
                </button>
            </div>
        </form>
    )
}


FieldLevelValidationForm = reduxForm({
    form: 'FieldLevelValidationForm' // a unique identifier for this form
})(FieldLevelValidationForm)

// You have to connect() to any reducers that you wish to connect to yourself
FieldLevelValidationForm = connect(

    state => ({
        initialValues: state.rootReducer.data.comment // pull initial values from account reducer
    })/*,
    {load: loadAccount}*/ // bind account loading action creator
)(FieldLevelValidationForm)

export default FieldLevelValidationForm;
