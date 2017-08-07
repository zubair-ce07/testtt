import { connect } from "react-redux";
import { getProfileStart } from "../actions";
import App from "./App";

function mapDispatchToProps(dispatch) {
  return {
    getProfile: username => {
      dispatch(getProfileStart(username));
    }
  };
}

function mapStateToProps(state) {
  return {
    profile: state.profile,
    hierarchy: state.hierarchy
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(App);
