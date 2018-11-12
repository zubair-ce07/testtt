import React from 'react';


function  VideoListObject(props) {
  const thumbnail = props.videoIcon.thumbnail
  const title = props.videoIcon.title

  return (
    <div className="card video-list-object"
      onClick={() => {props.onSelect(props.videoIcon)}}>
      <img
        className="card-img-top"
        src={thumbnail}
        alt="video"
      />
      <div className="card-body">
        <p className="card-text">{title}</p>
      </div>
    </div>
  )
}


export default VideoListObject;
