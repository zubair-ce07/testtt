import React from "react";
import { HealthBar } from "./components";
import "./HealthStatus.css";

const HealthStatus = props => {
  const { user, opponent } = props.data;
  return (
    <div className="health-status">
      <HealthBar content={user.content} percentage={user.percentage} />
      <HealthBar content={opponent.content} percentage={opponent.percentage} />
    </div>
  );
};

export { HealthStatus };
