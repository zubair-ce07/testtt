import React from "react"

const ErrorDetail = ({ errors }) => {
  const errorsList = []
  parseErrors(errors, errorsList)

  return errorsList.length ? (
    <div className="alert alert-danger" role="alert">
      <h4 className="alert-heading">Errors: </h4>
      <ul className="list-group list-group-flush">
        {errorsList.map((error, index) => (
          <li key={index} className="list-group-item">
            {error.toString()}
          </li>
        ))}
      </ul>
    </div>
  ) : null
}

const parseErrors = (errors, errorsList) => {
  if (errors === null) return errorsList

  if (typeof errors === "object") {
    for (const property in errors) {
      parseErrors(errors[property], errorsList)
    }
  } else if (Array.isArray(errors)) {
    for (const value of errors) {
      parseErrors(value, errorsList)
    }
  } else {
    return errorsList.push(errors.toString())
  }
}

export default ErrorDetail
