import React from 'react';
import VideoListObject from './videoListObject.js'


function  VideoList ({ sources, onSelect }) {
  let videosList = sources.map (
    (icon,i) => {
      if(icon)
        return (
          <li className="col-sm-2" key={i} >
            <VideoListObject
              videoIcon={icon}
              onSelect={onSelect}
            />
          </li>
        )
      else
        return null
    }
  )
  return <ul className="row video-list">{ videosList }</ul>
}


export default VideoList;
