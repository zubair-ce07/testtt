import React from 'react';
import VideoListObject from './videoListObject.js';

const VideoList = ({ sources, onSelect }) => {
  if (!sources) return null;
  let videosList = sources.map(icon => {
    return (
      <li className="col-sm-2" key={icon.id}>
        <VideoListObject videoIcon={icon} onSelect={onSelect} />
      </li>
    );
  });
  return <ul className="row video-list">{videosList}</ul>;
};

export default VideoList;
