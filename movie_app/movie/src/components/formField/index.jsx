import React from "react";
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

export { FormField };
