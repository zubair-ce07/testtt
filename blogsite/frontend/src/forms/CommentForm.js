import React, {Component} from 'react'
import { Field, reduxForm } from 'redux-form'
import {connect} from 'react-redux'
import {addComment, updateComment} from "../actions/comment";


class CommentsForm extends Component {
    constructor(props) {
        super(props);
        this.handleCommentSubmit = this.handleCommentSubmit.bind(this);

    }

    handleCommentSubmit(comment) {
       if(this.props.commentFormType==='create') this.props.addComment(comment)
        else this.props.updateComment(comment);
    }

    render() {
        const { handleSubmit, pristine, reset, submitting,commentFormType} = this.props;

        return (
            <form onSubmit={handleSubmit(this.handleCommentSubmit)}>

                <div>
                    <label>Name</label>
                    <div>
                        <Field name='author' component='input' type='text' placeholder='Name' disabled={commentFormType==='edit'}/>
                    </div>
                </div>

                <div>
                    <label>Comment</label>
                    <div>
                        <Field name='body' component='textarea' />
                    </div>
                </div>
                <div>
                    <button type='submit' disabled={pristine || submitting}>
                        Comment
                    </button>
                    <button type='button' disabled={pristine || submitting} onClick={reset}>
                        Undo
                    </button>
                </div>
            </form>
        )
    }

}
function mapStateToProps(state){
    return {
        initialValues: state.rootReducer.posts.comment,
        commentFormType:state.rootReducer.posts.commentFormType

    };
}
const mapDispatchToProps = (dispatch) => {
    return {
        addComment: (comment) => {
         dispatch(addComment(comment))
        },
        updateComment: (comment) => {
            dispatch(updateComment(comment))

        }
    }
}
CommentsForm = reduxForm({
    form: 'CommentsForm',
    enableReinitialize : true
})(CommentsForm)

CommentsForm = connect(
    mapStateToProps,
    mapDispatchToProps
)(CommentsForm)
export default CommentsForm


