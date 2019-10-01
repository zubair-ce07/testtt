import React from "react";

const Button = ({ text, onClick, type }) => (
  <button className={`btn btn-block ${type}`} onClick={onClick}>
    {text}
  </button>
);

export { Button };
