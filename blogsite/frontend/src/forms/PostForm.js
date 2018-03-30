import React, {Component} from 'react';
import { Field, reduxForm } from 'redux-form';
import { connect } from 'react-redux';
import {addPost, editPost} from '../actions/post';

const renderField = ({ input, label, type, meta: { touched, error } }) => (
    <div>
        <label>{label}</label>
        <div>
            <input {...input} placeholder={label} type={type} />
            {touched && error && <span>{error}</span>}
        </div>
    </div>
);

class PostForm extends Component {
    constructor(props) {
        super(props);
        this.handlePostSubmit = this.handlePostSubmit.bind(this);

    }

    handlePostSubmit(post) {
        if(this.props.postFormType==='create') this.props.addPost(post)
        else this.props.updatePost(post);
    }
    render(){
        const { error, handleSubmit,pristine,submitting, reset, postFormType } = this.props;
        return (
            <form onSubmit={handleSubmit(this.handlePostSubmit)}>

                <Field name='author'   type='text' component='input' label='Name' disabled={postFormType==='edit'}/>
                <Field name='title'    type='text' component={renderField} label='Title'/>
                <Field name='body'     type='text' component={renderField} label='Details'/>
                <div><label>Category</label></div>
                <Field name='category' component='select'>

                    <option value='redux'>redux</option>
                    <option value='react'>react</option>
                    <option value='udacity'>udacity</option>
                </Field>


                {error && <strong>{error}</strong>}
                <div>
                    <button type='submit' disabled={pristine || submitting}>Done</button>
                    <button type='button' disabled={pristine || submitting} onClick={reset}>Undo</button>
                </div>
            </form>
        );
    }

};

function mapStateToProps(state){
    return {
        initialValues: state.rootReducer.posts.post,
        postFormType:state.rootReducer.posts.postFormType

    };
}
const mapDispatchToProps = (dispatch) => {
    return {
        addPost: (post) => {
            dispatch(addPost(post))
        },
        updatePost: (post) => {
            dispatch(editPost(post))

        }
    }
}

PostForm = reduxForm({
    form: 'PostForm',
    enableReinitialize : true
})(PostForm);

PostForm = connect(
    mapStateToProps,
    mapDispatchToProps
)(PostForm);

export default PostForm;
