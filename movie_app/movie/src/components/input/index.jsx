import React from "react";
import "./input.css";

const Input = ({ field, type, icon, name, onChange, ...rest }) => (
  <div className="form-group">
    <div className="input-container">
      <i className={`fa ${icon} icon`} />
      <input
        {...rest}
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

export { Input };
