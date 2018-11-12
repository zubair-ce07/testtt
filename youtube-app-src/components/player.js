import React, { Component } from 'react';
import * as constants from '../constants.js';


class Player extends Component {
  constructor(props) {
    super(props)
    this.state = {
      source: props.source
    }
  }

  render() {
    if(!this.props.source)
      return <div></div>

    const url = `${constants.BASE_SOURCE}${this.props.source.videoId}`
    const title = this.props.source.title
    const description = this.props.source.description

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
}


export default Player;
