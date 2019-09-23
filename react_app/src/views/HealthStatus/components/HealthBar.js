import React from "react";
import { Label, Card } from "../../../components";
import { ProgressBar } from ".";
const HealthBar = props => {
  const { content, percentage } = props;
  return (
    <Card>
      <Label text={content} />
      <ProgressBar percentage={percentage} />
      <Label text={percentage} />
    </Card>
  );
};

export { HealthBar };
