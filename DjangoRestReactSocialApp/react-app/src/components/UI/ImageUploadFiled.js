import React from 'react'
import PropTypes from 'prop-types'

const ImageUploadField = ({
  field, // { name, value, onChange, onBlur }
  form: { touched, errors, setFieldValue }, // also values, setXXXX, handleXXXX, dirty, isValid, status, etc.
  ...props
}) => (
  <div>
    <input id={field.name} name={field.name} type="file" onChange={(event) => {
      setFieldValue(field.name, event.currentTarget.files[0])
    }}/>
    <label className="custom-file-label" htmlFor="image">Upload image</label>
    {touched[field.name] &&
        errors[field.name] && <div className="error">{errors[field.name]}</div>}
  </div>
)

ImageUploadField.propTypes = {
  field: PropTypes.any,
  form: PropTypes.any
}

export default ImageUploadField
