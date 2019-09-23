import React from "react";
import { Filler } from "../";
import "./ProgressBar.css";

const ProgressBar = props => (
  <div className="progress-bar">
    <Filler percentage={props.percentage} />
  </div>
);

export { ProgressBar };
