import { ErrorMessage, Field } from "formik"
import React, { Component } from "react"

import Select from "react-select"

export class CustomSelect extends Component {
  handleChange = value => {
    const { onChange, name } = this.props
    onChange(name, value)
  }
  handleBlur = () => {
    const { onBlur, name } = this.props
    onBlur(name, true)
  }

  render() {
    const { id, isMutli, label, name, options, paceholder, value } = this.props

    return (
      <div className="form-group">
        <label htmlFor={name}>{label}</label>
        <Select
          id={id}
          name={name}
          options={options}
          placeholder={paceholder}
          isMulti={isMutli}
          value={value}
          onChange={this.handleChange}
          onBlur={this.handleBlur}
        />
        <ErrorMessage component="p" name={name} className="text-danger" />
      </div>
    )
  }
}

export const CustomField = props => {
  const { name, label, placeholder, type } = props
  return (
    <div className="form-group">
      <label htmlFor="title">{label}</label>
      <Field
        type={type}
        name={name}
        className="form-control"
        placeholder={placeholder}
      />
      <ErrorMessage component="p" name={name} className="text-danger" />
    </div>
  )
}
