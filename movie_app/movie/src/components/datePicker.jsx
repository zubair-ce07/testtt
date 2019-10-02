import React from "react";

const DatePicker = ({ name, onChange, ...rest }) => (
  <div className="form-group">
    <input
      {...rest}
      type="date"
      name={name}
      className="form-control"
      onChange={onChange}
    />
  </div>
);

export { DatePicker };
