import React, { useState } from 'react'
import PropTypes from 'prop-types'

import { resolveImageUrl } from 'helpers/common'

const ImageUploadField = ({
  field,
  form: { touched, errors, setFieldValue },
  post,
  ...props
}) => {
  const [file, fileChange] = useState(null)
  const randomId = Math.floor(Math.random() * 10000)
  return (
    <>
      <input className="image-post" id={`${field.name}${randomId}`} name={field.name} type="file" onChange={(event) => {
        setFieldValue(field.name, event.currentTarget.files[0])
        fileChange(URL.createObjectURL(event.currentTarget.files[0]))
      }}/>
      {
        field.value && !field.value.name && post
          ? <>
            <label className="custom-file-label" htmlFor={`${field.name}${randomId}`}>{field.value ? field.value.name : 'Upload image'}</label>
            <img className="previewImage" src={resolveImageUrl(post.image)} alt="preview"/>
          </>
          : <>
            <label className="custom-file-label" htmlFor={`${field.name}${randomId}`}>{field.value ? field.value.name : 'Upload image'}</label>
            <img className="previewImage" src={file} alt="preview"/>
          </>
      }
      {/* <label className="custom-file-label" htmlFor={`${field.name}${randomId}`}>{field.value ? field.value.name : 'Upload image'}</label>
      <img className="previewImage" src={file} alt="preview"/> */}
      {touched[field.name] &&
        errors[field.name] && <div className="error">{errors[field.name]}</div>}
    </>
  )
}

ImageUploadField.propTypes = {
  field: PropTypes.any,
  form: PropTypes.any,
  post: PropTypes.any
}

export default ImageUploadField
