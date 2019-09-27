import React from "react";
import PropTypes from "prop-types";

const Button = ({ text, onClick}) => (
  <button className="btn btn-primary" onClick={onClick}>{text}</button>
);

Button.PropTypes = {
  text: PropTypes.string.isRequired
};

export { Button };
