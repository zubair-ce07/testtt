import { isEmpty } from 'underscore';
import React from 'react';
import { object } from 'prop-types';
import { YOUTUBE_VIDEO_PLAY_URL } from '../../configs/';
import Loading from '../common/Loading';

const VideoPlay = ({ video }) => {
  // Play video component

  if (isEmpty(video)) {
    return <Loading />
  }

  const videoUrl = `${YOUTUBE_VIDEO_PLAY_URL}${video.id.videoId}`;
  const { title, description } = video.snippet;

  return (
    <div className="video-play col-md-8 col-sm-12">
      <div className="embed-responsive embed-responsive-16by9">
        <iframe
          className="embed-responsive-item"
          src={videoUrl}
          title={title}
        ></iframe>
      </div>
      <div className="details">
        <div className='left-allign'>{title}</div>
        <div className='left-allign grey-small'>{description}</div>
      </div>
    </div>
  )
};

VideoPlay.propTypes = {
  video: object.isRequired
};

export default VideoPlay
