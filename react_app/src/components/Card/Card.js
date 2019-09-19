import React from "react";
import "./Card.css";

const Card = props => {
  return (
    <div className="card">
      <div className="content">{props.children}</div>
    </div>
  );
};

export { Card };
