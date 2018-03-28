import React from 'react';
import { Field, reduxForm } from 'redux-form';
import { connect } from 'react-redux';

const renderField = ({ input, label, type, meta: { touched, error } }) => (
    <div>
        <label>{label}</label>
        <div>
            <input {...input} placeholder={label} type={type} />
            {touched && error && <span>{error}</span>}
        </div>
    </div>
);

let PostForm = props => {
console.log(props)
    const { error, handleSubmit,pristine,submitting, reset, mode } = props;
    return (
        <form onSubmit={handleSubmit}>

            <Field name='author'   type='text' component='input' label='Name' disabled={mode==='edit'}/>
            <Field name='title'    type='text' component={renderField} label='Title'/>
            <Field name='body'     type='text' component={renderField} label='Details'/>
            <div><label>Category</label></div>
                    <Field name="category" component="select">

                        <option value="redux">redux</option>
                        <option value="react">react</option>
                        <option value="udacity">udacity</option>
                    </Field>


            {error && <strong>{error}</strong>}
            <div>
                <button type="submit" disabled={pristine || submitting}>Done</button>
                <button type="button" disabled={pristine || submitting} onClick={reset}>Undo</button>
            </div>
        </form>
    );
};

PostForm = reduxForm({
    form: 'PostForm',
    enableReinitialize : true
})(PostForm);

PostForm = connect(
    state => ({
        initialValues: state.rootReducer.posts.post
    })
)(PostForm);

export default PostForm;
