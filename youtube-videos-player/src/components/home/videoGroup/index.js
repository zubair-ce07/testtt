import React from 'react';
import { func, array } from 'prop-types';
import VideoGroupItem from './VideoGroupItem';

const VideoGroup = ({ videos, playVideo }) => {
  // Video group component

  return (
    <div className="col-md-4">
      <ul className="list-group">
        {videos.map((videoItem) => (
          <VideoGroupItem
            key={videoItem.id.videoId}
            videoItem={videoItem}
            playVideo={playVideo}
          />
        ))}
      </ul>
    </div>
  );
};

VideoGroup.propTypes = {
  videos: array.isRequired,
  playVideo: func.isRequired
};

export default VideoGroup
