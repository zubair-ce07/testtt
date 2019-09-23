import React from "react";
import { HealthBar } from "./components";
import "./HealthStatus.css";

const HealthStatus = props => (
  <div className="health-status">
    <HealthBar
      content={props.data.user.content}
      percentage={props.data.user.percentage}
    />
    <HealthBar
      content={props.data.opponent.content}
      percentage={props.data.opponent.percentage}
    />
  </div>
);

export { HealthStatus };
