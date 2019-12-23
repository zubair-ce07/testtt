import React from 'react'
import PropTypes from 'prop-types'
import TextFieldMat from '@material-ui/core/TextField'

const TextareaField = ({
  field,
  form: { touched, errors },
  label,
  ...props
}) => (
  <div>
    <TextFieldMat
      {...props}
      {...field}
      label={label}
      multiline

      helperText={(errors[field.name] && touched[field.name]) && errors[field.name]}
      error={touched[field.name] && errors[field.name]}
      margin="normal"
    />

  </div>
)

TextareaField.propTypes = {
  field: PropTypes.any,
  form: PropTypes.any,
  label: PropTypes.any
}

export default TextareaField
