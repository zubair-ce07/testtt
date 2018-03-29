import React, {Component} from 'react'
import { Field, reduxForm } from 'redux-form'
import {connect} from 'react-redux'

class CommentsForm extends Component {
   
    render() {

        const { handleSubmit, pristine, reset, submitting ,mode} = this.props
        return (
            <form onSubmit={handleSubmit}>

                <div>
                    <label>Name</label>
                    <div>
                        <Field name="author" component="input" type="text" placeholder='Name' disabled={mode==='edit'}/>
                    </div>
                </div>

                <div>
                    <label>Comment</label>
                    <div>
                        <Field name="body" component="textarea" />
                    </div>
                </div>
                <div>
                    <button type="submit" disabled={pristine || submitting}>
                        Comment
                    </button>
                    <button type="button" disabled={pristine || submitting} onClick={reset}>
                        Undo
                    </button>
                </div>
            </form>
        )
    }

}


CommentsForm = reduxForm({
    form: 'CommentsForm',
    enableReinitialize : true
})(CommentsForm)

CommentsForm = connect(
    state => ({
        initialValues: state.rootReducer.posts.comment
    })
)(CommentsForm)
export default CommentsForm


