import React from "react";
import DynamicImage from "./dynamicImage";
import { smallSize } from "./styles";

const IconItem = props => {
  const { iconItem } = props;
  const iconName = `icon-${iconItem.iconNameSuffix}.png`;

  return (
    <div className="d-flex flex-column card m-3 bg-primary">
      <DynamicImage style={smallSize} name={iconName} />
      <div className="card-body text-center">
        <h6 className="card-title">{iconItem.label}</h6>
      </div>
    </div>
  );
};

export default IconItem;
