import React from 'react';
import Image from './videoImage.js"';

const VideoListObject = ({ videoIcon, onSelect }) => {
  return (
    <div
      className="card video-list-object"
      onClick={() => {
        onSelect(videoIcon);
      }}
    >
      <Image src={videoIcon.thumbnail} />
      <span className="card-body">
        <p className="card-text">{videoIcon.title}</p>
      </span>
    </div>
  );
};

export default VideoListObject;
