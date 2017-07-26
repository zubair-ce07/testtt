import { connect } from "react-redux";
import { playVideo } from "../../actions";
import Result from "./Result";

function mapDispatchToProps(dispatch) {
  return {
    onResultClick: vidId => {
      dispatch(playVideo(vidId));
    }
  };
}

function mapStateToProps(state) {
  return {
    results: state.results
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(Result);
