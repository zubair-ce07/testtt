import React from 'react';
import VideoListObject from './videoListObject.js'


function  VideoList(props) {
  let videosList = props.sources.map (
    (icon,i) => {
      if(icon)
        return (
          <li className="col-sm-2" key={i} >
            <VideoListObject
              videoIcon={icon}
              onSelect={props.onSelect}
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
