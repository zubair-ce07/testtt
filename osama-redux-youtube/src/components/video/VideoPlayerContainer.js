import { connect } from "react-redux";
import VideoPlayer from "./VideoPlayer";

function mapStateToProps(state) {
  return {
    playVid: state.playVid,
    vidId: state.vidId
  };
}

export default connect(mapStateToProps)(VideoPlayer);
