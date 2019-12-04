import React from 'react'
import PropTypes from 'prop-types'

const TextareaField = ({
  field, // { name, value, onChange, onBlur }
  form: { touched, errors }, // also values, setXXXX, handleXXXX, dirty, isValid, status, etc.
  ...props
}) => (
  <div>
    <textarea type="text" {...field} {...props} />
    {touched[field.name] &&
        errors[field.name] && <div className="error">{errors[field.name]}</div>}
  </div>
)

TextareaField.propTypes = {
  field: PropTypes.any,
  form: PropTypes.any
}

export default TextareaField
