import React from "react";
import "./VideoPlayer.css";

class VideoPlayer extends React.Component {
  constructor(props) {
    super();
    this.state = {
      play: props.play,
      vidId: props.vidId
    };
  }
  render() {
    if (this.state.vidId !== false) {
      return (
        <iframe
          title="playerFrame"
          className="player"
          width="854"
          height="480"
          src={"https://www.youtube.com/embed/" + this.state.vidId}
          frameBorder="0"
          allowFullScreen
        />
      );
    } else return null;
  }
}

export default VideoPlayer;
