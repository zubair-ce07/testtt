import React from 'react'
import { useDispatch } from 'react-redux'
import { Formik, Form, Field } from 'formik'
import * as Yup from 'yup'

import TextareaField from 'components/UI/TextareaField'
import ImageUploadField from 'components/UI/ImageUploadFiled'

import { createPost } from 'store/modules/post/post.action'

import { toast } from 'helpers/common'

const SUPPORTED_FORMATS = ['image/jpg', 'image/jpeg', 'image/gif', 'image/png']
const Schema = Yup.object().shape({
  title: Yup.string().min(2, 'Too Short!').max(50, 'Too Long!').required('Required'),
  body: Yup.string().min(10, 'Too Short!').required('Required'),
  image: Yup.mixed().test('fileType', 'Unsupported File Format', value => value && SUPPORTED_FORMATS.includes(value.type))
})

export const CreatePost = props => {
  const dispatch = useDispatch()
  return (
    <Formik
      initialValues={{ title: '', body: '' }}
      validationSchema={Schema}
      onSubmit={values => {
        console.log(values)
        dispatch(createPost(values)).then((res) => {
          if (res.value.data.status) {
            toast('success', 'Post Added Successfully')
          } else {
            toast('success', 'Error while adding post')
          }
        })
      }}
    >
      {({ errors, touched, setFieldValue }) => (
        <Form>
          <div className="card gedf-card">
            <div className="card-header">
              <ul className="nav nav-tabs card-header-tabs" id="myTab" role="tablist">
                <li className="nav-item">
                  <a className="nav-link active" id="posts-tab" data-toggle="tab" href="#posts" role="tab"
                    aria-controls="posts" aria-selected="true">Make a publication</a>
                </li>
                <li className="nav-item">
                  <a className="nav-link" id="images-tab" data-toggle="tab" role="tab" aria-controls="images"
                    aria-selected="false" href="#images">Image</a>
                </li>
              </ul>
            </div>
            <div className="card-body">
              <div className="tab-content" id="myTabContent">
                <div className="tab-pane fade show active" id="posts" role="tabpanel" aria-labelledby="posts-tab">
                  <div className="form-group">
                    <label className="sr-only" htmlFor="message">Title</label>
                    <Field type="text" name="title" className="form-control" placeholder="Post title"/>
                    <label className="sr-only" htmlFor="message">Post</label>
                    <Field name="body" className="form-control" component={TextareaField} placeholder="What are you thinking?"></Field>
                  </div>

                </div>
                <div className="tab-pane fade" id="images" role="tabpanel" aria-labelledby="images-tab">
                  <div className="form-group">
                    <div className="custom-file">
                      <Field name="image" component={ImageUploadField}/>
                    </div>
                  </div>
                  <div className="py-4"></div>
                </div>
              </div>
              <div className="btn-toolbar justify-content-between">
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

export default CreatePost
