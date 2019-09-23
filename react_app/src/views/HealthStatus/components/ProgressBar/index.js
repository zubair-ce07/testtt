import React from "react";
import "./ProgressBar.css";

const ProgressBar = ({percentage}) => (
  <div className="progress-bar">
    <div className="filler" style={{ width: `${percentage}%` }} />
  </div>
);

export { ProgressBar };
