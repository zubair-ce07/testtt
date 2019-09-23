import React from "react";

const Button = props => (
  <button className="ui basic button" onClick={props.onClick}>
    {props.text}
  </button>
);

export { Button };
