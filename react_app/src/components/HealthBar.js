import React from "react";
import { Label, Card, ProgressBar} from ".";

const HealthBar = props => {
  return (
    <Card>
      <Label content={props.content} />
      <ProgressBar percentage={props.percentage} />
      <Label content={props.percentage} />
    </Card>
  );
};

export { HealthBar };
