import React from "react";
import SimpleSelect from "@material-ui/core/Select";

const Select = ({ options }) => {
  const selectOptions = options.map(option => {
    return <option value={option}>{option}</option>;
  });
  return <SimpleSelect displayEmpty={true} children={selectOptions} />;
};

export { Select };
