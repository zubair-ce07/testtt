import React from 'react';
import { string, shape, func } from 'prop-types';

import Image from './videoImage';

const VideoListObject = ({ videoIcon, onSelect }) => {
  return (
    <div
      className="card video-list-object"
      onClick={() => {
        onSelect(videoIcon);
      }}
    >
      <Image source={videoIcon.thumbnail} />
      <span className="card-body">
        <p className="card-text">{videoIcon.title}</p>
      </span>
    </div>
  );
};

VideoListObject.propTypes = {
  videoIcon: string
};

VideoListObject.propTypes = {
  videoIcon: shape({
    title: string,
    description: string,
    id: string,
    thumbnail: string
  }),
  onSelect: func
};

export default VideoListObject;
