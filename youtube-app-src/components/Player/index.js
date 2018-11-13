import React from 'react';
import * as constants from '../../constants.js';


function  Player (props) {
  if(!props.source)
    return null

  const { source: { title, description, videoId}} = props
  const url = `${constants.BASE_SOURCE}${videoId}`

  return (
    <div className="main-player row">
      <iframe className="col-sm-9"
        title={title}
        src={url}
      >
      </iframe>
      <div className="card col-sm-3 player-detail">
        <div className="card-body">
          <h4 className="card-title player-title">
            {title}
          </h4>
          <p className="card-text player-description">
            {description}
          </p>
        </div>
      </div>
    </div>
  )
}


export default Player;
