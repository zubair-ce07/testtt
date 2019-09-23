import React from "react";
import { Label, Card } from "../../../components";
import { ProgressBar } from ".";
const HealthBar = props => (
  <Card>
    <Label text={props.content} />
    <ProgressBar percentage={props.percentage} />
    <Label text={props.percentage} />
  </Card>
);

export { HealthBar };
