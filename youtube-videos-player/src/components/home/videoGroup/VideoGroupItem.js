import React from 'react';
import { object, func } from 'prop-types';

const VideoGroupItem = ({ videoItem, playVideo }) => {
  // Video group component

  const url = videoItem.snippet.thumbnails.default.url;
  const { title, publishedAt } = videoItem.snippet;

  return (
    <li onClick={() => playVideo(videoItem)} className="videos-list-item">
      <div className="video-list media">
        <div className="media-left">
          <img
            className="media-object border-round"
            alt={title}
            src={url}
          />
        </div>
        <div className="media-body">
          <div className="media-heading white-large">{title}</div>
          <div className="video-publisher-date grey-small">
            Published on: {(new Date(publishedAt)).toDateString()}
          </div>
        </div>
      </div>
    </li>
  );
};

VideoGroupItem.propTypes = {
  videoItem: object.isRequired,
  playVideo: func.isRequired
};

export default VideoGroupItem
