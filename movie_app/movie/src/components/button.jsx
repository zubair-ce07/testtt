import React from "react";

const Button = ({ text, onClick, type }) => (
  <button className={`btn ${type}`} onClick={onClick}>
    {text}
  </button>
);

export { Button };
