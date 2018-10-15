import { isEmpty } from 'underscore';
import React from 'react';
import { object } from 'prop-types';
import { youtubeVideoPlayUrl } from '../../configs/';
import Loading from '../common/Loading';

const VideoPlay = (props) => {
  // Play video component

  const video = props.video;

  // Checks if there is no video to play
  if (isEmpty(video)) {
    return <Loading />
  }

  const videoUrl = `${youtubeVideoPlayUrl}${video.id.videoId}`;
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
