import React from 'react';
import { string } from 'prop-types';

const VideoImage = ({ source }) => {
  return <img className="card-img-top" src={source} alt={source} />;
};

VideoImage.propTypes = {
  source: string
};

export default VideoImage;
