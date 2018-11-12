import React from 'react';


function  VideoListObject(props) {
  return (
    <div className="card video-list-object"
      onClick={() => {props.onSelect(props.videoIcon)}}>
      <img
        className="card-img-top"
        src={props.videoIcon.thumbnail}
        alt="video"
      />
      <div className="card-body">
        <p className="card-text">{props.videoIcon.title}</p>
      </div>
    </div>
  )
}


export default VideoListObject;
