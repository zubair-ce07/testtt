import React from "react";

const Button = props => {
  const { onClick, text } = props;
  return (
    <button className="ui basic button" onClick={onClick}>
      {text}
    </button>
  );
};

export { Button };
