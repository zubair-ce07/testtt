import React, { useState } from 'react'
import PropTypes from 'prop-types'

const ImageUploadField = ({
  field,
  form: { touched, errors, setFieldValue },
  ...props
}) => {
  const [file, fileChange] = useState(null)
  return (
    <>
      <input id={field.name} name={field.name} type="file" onChange={(event) => {
        setFieldValue(field.name, event.currentTarget.files[0])
        fileChange(URL.createObjectURL(event.currentTarget.files[0]))
      }}/>
      <label className="custom-file-label" htmlFor="image">{field.value ? field.value.name : 'Upload image'}</label>
      <img className="previewImage" src={file}/>
      {touched[field.name] &&
        errors[field.name] && <div className="error">{errors[field.name]}</div>}
    </>
  )
}

ImageUploadField.propTypes = {
  field: PropTypes.any,
  form: PropTypes.any
}

export default ImageUploadField
