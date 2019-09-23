import React from "react";
import "./Card.css";

const Card = props => (
  <div className="card">
    <div className="content">{props.children}</div>
  </div>
);

export { Card };
