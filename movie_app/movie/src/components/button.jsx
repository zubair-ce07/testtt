import React from "react";

const Button = ({ text, onClick, type, className }) => (
  <button type={type} className={`btn ${className}`} onClick={onClick}>
    {text}
  </button>
);

export { Button };
