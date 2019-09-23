import React from "react";
import "./Filler.css";

const Filler = props => (
  <div className="filler" style={{ width: `${props.percentage}%` }} />
);

export { Filler };
