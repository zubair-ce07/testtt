import React from 'react'
import PropTypes from 'prop-types'

export const ActionComponent = ({ actionHandler }) => {
  return (

    <div className="dropdown">
      <button className="btn btn-link dropdown-toggle" type="button" id="gedf-drop1" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
        <i className="fa fa-ellipsis-h"></i>
      </button>

      <div className="dropdown-menu dropdown-menu-right" aria-labelledby="gedf-drop1">
        <div className="h6 dropdown-header">Configuration </div>
        <span className="dropdown-item" onClick={() => { actionHandler('edit') }} >Edit</span>
        <span className="dropdown-item" onClick={() => { actionHandler('delete') }} >Delete</span>
      </div>
    </div>
  )
}

ActionComponent.propTypes = {
  actionHandler: PropTypes.any
}

export default ActionComponent
