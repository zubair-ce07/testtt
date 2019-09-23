import React from "react";
import "./Card.css";

const Card = ({children}) => (
  <div className="card">
    <div className="content">{children}</div>
  </div>
);

export { Card };
