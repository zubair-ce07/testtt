import React from "react";
import PropTypes from "prop-types";

const Label = ({ text }) => <label className="form-group">{text}</label>;

Label.PropTypes = {
  text: PropTypes.string.isRequired
};

export { Label };
