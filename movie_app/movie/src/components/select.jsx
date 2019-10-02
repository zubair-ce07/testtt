import React from "react";

const Select = ({ items, name, field, onChange, ...rest }) => (
  <div className="form-group">
    <select
      {...rest}
      className="form-control"
      name={name}
      onChange={onChange}
      defaultValue="Gender"
    >
      <option disabled>{field}</option>
      {items.map(item => (
        <option key={item} value={item}>
          {item}
        </option>
      ))}
    </select>
  </div>
);

export { Select };
