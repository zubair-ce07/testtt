import React from "react";
import PropTypes from "prop-types";
import "./VideoPlayer.css";

class VideoPlayer extends React.Component {
  render() {
    return (
      <div className="player-container">
        <iframe
          title="playerFrame"
          className="player"
          src={
            "https://www.youtube.com/embed/" + this.props.vidId + "?autoplay=1"
          }
          frameBorder="0"
          allowFullScreen
        />
      </div>
    );
  }
}

VideoPlayer.propTypes = {
  vidId: PropTypes.string.isRequired
};

export default VideoPlayer;
