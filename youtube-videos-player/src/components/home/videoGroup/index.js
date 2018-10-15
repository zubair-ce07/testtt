import React from 'react';
import { func, array } from 'prop-types';
import VideoGroupItem from './VideoGroupItem';

const VideoGroup = (props) => {
  // Video group component

  const { videos, playVideo } = props;
  const videoItems = videos.map((videoItem) => {
    return (
      <VideoGroupItem
        key={videoItem.id.videoId}
        videoItem={videoItem}
        playVideo={playVideo}
      />
    );
  });

  return (
    <div className="col-md-4">
      <ul className="list-group">
        {videoItems}
      </ul>
    </div>
  );
};

VideoGroup.propTypes = {
  videos: array.isRequired,
  playVideo: func.isRequired
};

export default VideoGroup
