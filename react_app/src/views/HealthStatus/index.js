import React from "react";
import { HealthBar } from "./components";
import "./HealthStatus.css";

const HealthStatus = ({ data: { user, opponent } }) => (
  <div className="health-status">
    <HealthBar content={user.content} percentage={user.percentage} />
    <HealthBar content={opponent.content} percentage={opponent.percentage} />
  </div>
);

export { HealthStatus };
