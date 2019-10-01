import React from "react";

const DatePicker = ({ name, onChange }) => (
  <div className="form-group">
    <input
      type="date"
      name={name}
      className="form-control"
      onChange={onChange}
    />
  </div>
);

export { DatePicker };
