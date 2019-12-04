import React from 'react'
import { useDispatch } from 'react-redux'
import PropTypes from 'prop-types'
import { Formik, Form, Field } from 'formik'
import * as Yup from 'yup'

import TextareaField from 'components/UI/TextareaField'

import { createComment, updateComment } from 'store/modules/comment/comment.action'

import { toast } from 'helpers/common'

const Schema = Yup.object().shape({
  comment: Yup.string().min(10, 'Too Short!').required('Required')
})

export const CreateComment = ({ post, mode, comment, modeChange }) => {
  const dispatch = useDispatch()
  return (
    <Formik
      initialValues={{ comment: mode === 'edit' ? comment.comment : '' }}
      validationSchema={Schema}
      onSubmit={values => {
        console.log(values)
        values.post = post.id
        if (mode === 'edit') {
          dispatch(updateComment(values, comment.id)).then((res) => {
            if (res.value.data.status) {
              toast('success', 'Comment Updated Successfully')
              modeChange('view')
            } else {
              toast('success', 'Error while adding comment')
            }
          })
        } else {
          dispatch(createComment(values)).then((res) => {
            if (res.value.data.status) {
              toast('success', 'Comment Added Successfully')
            } else {
              toast('success', 'Error while adding comment')
            }
          })
        }
      }}
    >
      {({ errors, touched, setFieldValue }) => (
        <div className="col-md-12 clearfix">
          <Form>
            <Field name="comment" component={TextareaField} className="form-control" placeholder="write a comment..." rows="3"></Field>
            <br/>
            <button type="submit" className="btn btn-info pull-right">Post</button>
          </Form>
        </div>
      )}
    </Formik>

  )
}

CreateComment.propTypes = {
  comment: PropTypes.any,
  mode: PropTypes.any,
  modeChange: PropTypes.any,
  post: PropTypes.any
}

export default CreateComment
