import React from "react";

const Button = props => {
  return (
    <button className="ui basic button" onClick={props.action}>
      {props.content}
    </button>
  );
};

export { Button };
