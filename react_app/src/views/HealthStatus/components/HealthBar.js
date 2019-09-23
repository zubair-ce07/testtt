import React from "react";
import { Label, Card } from "../../../components";
import { ProgressBar } from ".";
const HealthBar = ({ content, percentage }) => (
  <Card>
    <Label text={content} />
    <ProgressBar percentage={percentage} />
    <Label text={percentage} />
  </Card>
);

export { HealthBar };
