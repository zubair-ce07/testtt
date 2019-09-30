import React from "react";
import PropTypes from "prop-types";
import "./formField.css";

const FormField = ({ field, type, icon, name, onChange }) => (
  <div className="form-group">
    <div className="input-container">
      <i className={`fa ${icon} icon`} />
      <input
        required
        type={type}
        name={name}
        className="form-control"
        placeholder={field}
        onChange={onChange}
      />
    </div>
  </div>
);

FormField.propTypes = {
  field: PropTypes.string.isRequired,
  type: PropTypes.string.isRequired
};

export { FormField };
