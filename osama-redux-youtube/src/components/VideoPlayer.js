import React from "react";
import PropTypes from "prop-types";
import "./VideoPlayer.css";

class VideoPlayer extends React.Component {
  constructor(props) {
    super();
    this.dispatch = props.dispatch;
  }

  render() {
    return (
      <iframe
        title="playerFrame"
        className="player"
        src={
          "https://www.youtube.com/embed/" + this.props.vidId + "?autoplay=1"
        }
        frameBorder="0"
        allowFullScreen
      />
    );
  }
}

VideoPlayer.propTypes = {
  vidId: PropTypes.string.isRequired
};

export default VideoPlayer;
