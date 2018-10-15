import React from 'react';
import {array, func, object} from 'prop-types';
import Header from '../common/Header'
import VideoPlay from './VideoPlay';
import VideoGroup from './videoGroup/';

const Index = (props) => {
  // Home component

  const { videos, mainVideo, searchOnYoutube, playVideo } = props;

  return (
    <div className='row'>
      <Header
        searchOnYoutube={searchOnYoutube}
      />
      <div className="row">
        <VideoPlay video={mainVideo} />
        <VideoGroup
          videos={videos}
          playVideo={playVideo}
        />
      </div>
    </div>
  )
};

Index.propTypes = {
  videos: array.isRequired,
  mainVideo: object.isRequired,
  searchOnYoutube: func.isRequired,
  playVideo: func.isRequired,
};

export default Index
