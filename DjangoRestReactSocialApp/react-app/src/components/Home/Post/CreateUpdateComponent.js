import React from 'react'
import { useDispatch } from 'react-redux'
import PropTypes from 'prop-types'
import { Formik, Form, Field } from 'formik'
import * as Yup from 'yup'

import TextareaField from 'components/UI/TextareaField'
import ImageUploadField from 'components/UI/ImageUploadFiled'

import { createPost, updatePost } from 'store/modules/post/post.action'

import { toast } from 'helpers/common'
import TextField from 'components/UI/TextField'

const SUPPORTED_FORMATS = ['image/jpg', 'image/jpeg', 'image/gif', 'image/png']
const Schema = Yup.object().shape({
  title: Yup.string().min(2, 'Too Short!').max(50, 'Too Long!').required('Required'),
  body: Yup.string().min(10, 'Too Short!').required('Required'),
  image: Yup.mixed().test('fileType', 'Unsupported File Format', value => value && SUPPORTED_FORMATS.includes(value.type))
})

export const CreateUpdatePost = ({ mode, post, modeChange }) => {
  const dispatch = useDispatch()
  let initialValues = { title: '', body: '' }
  if (mode === 'edit') { initialValues = post }

  const resolveId = (id) => {
    if (mode === 'edit') {
      return id + post.id
    }
    return id
  }
  return (
    <Formik
      initialValues={initialValues}
      validationSchema={Schema}
      onSubmit={values => {
        console.log(values)
        if (mode === 'create') {
          dispatch(createPost(values)).then((res) => {
            if (res.value.data.status) {
              toast('success', 'Post Added Successfully')
            } else {
              toast('success', 'Error while adding post')
            }
          })
        } else {
          dispatch(updatePost(values, post.id)).then((res) => {
            if (res.value.data.status) {
              toast('success', 'Post Updated Successfully')
              modeChange('view')
            } else {
              toast('success', 'Error while updating post')
            }
          })
        }
      }}
    >
      {() => (
        <Form>
          <div className="card gedf-card">
            <div className="card-header">
              <ul className="nav nav-tabs card-header-tabs" id="myTab" role="tablist">
                <li className="nav-item">
                  <a className="nav-link active" id="posts-tab" data-toggle="tab" href={resolveId('#posts')} role="tab"
                    aria-controls="posts" aria-selected="true">Make a publication</a>
                </li>
                <li className="nav-item">
                  <a className="nav-link" id="images-tab" data-toggle="tab" role="tab" aria-controls="images"
                    aria-selected="false" href={resolveId('#images')}>Image</a>
                </li>
              </ul>
            </div>
            <div className="card-body">
              <div className="tab-content" id="myTabContent">
                <div className="tab-pane fade show active" id={resolveId('posts')} role="tabpanel" aria-labelledby="posts-tab">
                  <div className="form-group">
                    <Field name="title" className="form-control" component={TextField} label="Post title"></Field>
                  </div>
                  <div className="form-group">
                    <Field name="body" className="form-control" component={TextareaField} label="What are you thinking?"></Field>
                  </div>
                </div>
                <div className="tab-pane fade" id={resolveId('images')} role="tabpanel" aria-labelledby="images-tab">

                  <div className="custom-file">
                    <Field name="image" component={ImageUploadField}/>
                  </div>

                  <div className="py-4"></div>
                </div>
              </div>
              <div className="btn-toolbar ">
                <div className="btn-group">
                  <button type="submit" className="btn btn-primary">share</button>
                </div>
              </div>
            </div>
          </div>
        </Form>
      )}
    </Formik>

  )
}

CreateUpdatePost.propTypes = {
  mode: PropTypes.any,
  modeChange: PropTypes.any,
  post: PropTypes.any
}

export default CreateUpdatePost
