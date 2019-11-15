import React from "react";
var images = require.context("../../public/icons", true);

const DynamicImage = props => {
  const { style } = props;
  let img_src = images(`./${props.name}`);
  return (
    <img
      style={style}
      className="img-fluid img-thumbnail"
      src={img_src}
      alt=""
    />
  );
};

export default DynamicImage;
