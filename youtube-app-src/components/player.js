import React, { Component } from 'react';


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
    return (
      <div className="main-player row">
        <iframe className="col-sm-9"
          title={this.props.source.url}
          src={this.props.source.url}
        >
        </iframe>
        <div className="card col-sm-3 player-detail">
          <div className="card-body">
            <h4 className="card-title player-title">
              {this.props.source.title}
            </h4>
            <p className="card-text player-description">
              {this.props.source.description}
            </p>
          </div>
        </div>
      </div>
    )
  }
}


export default Player;
