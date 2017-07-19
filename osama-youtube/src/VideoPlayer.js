import React from "react";
import "./VideoPlayer.css";

class VideoPlayer extends React.Component {
  render() {
    return (
      <iframe
        title="playerFrame"
        className="player"
        width="854"
        height="480"
        src={"https://www.youtube.com/embed/" + this.props.vidId + "?autoplay=1"}
        frameBorder="0"
        allowFullScreen
        autoplay="1"
      />
    );
  }
}

export default VideoPlayer;
