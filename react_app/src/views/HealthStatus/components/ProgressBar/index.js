import React from "react";
import "./ProgressBar.css";

const ProgressBar = props => (
  <div className="progress-bar">
    <div className="filler" style={{ width: `${props.percentage}%` }} />
  </div>
);

export { ProgressBar };
