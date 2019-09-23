import React from "react";

const Button = ({ onClick, text }) => (
  <button className="ui basic button" onClick={onClick}>
    {text}
  </button>
);

export { Button };
