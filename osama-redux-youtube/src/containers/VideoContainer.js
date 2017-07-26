import React from "react";
import { connect } from "react-redux";
import VideoPlayer from "../components/VideoPlayer";

class VideoContainer extends React.Component {
  render() {
    if (this.props.playVid) {
      return (
        <div className="player-container">
          <VideoPlayer />
        </div>
      );
    } else {
      return null;
    }
  }
}

function mapStateToProps(state) {
  return {
    playVid: false,
    vidId: ""
  };
}

export default connect(mapStateToProps)(VideoContainer);
