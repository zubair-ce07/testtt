import { connect } from "react-redux";
import Hierarchy from "./Hierarchy";
import { replaceDirectsStart } from "../../actions";

function mapDispatchToProps(dispatch) {
  return {
    onClick: (username, hierarchy) => {
      dispatch(replaceDirectsStart(username, hierarchy));
    }
  };
}

function mapStateToProps(state) {
  return {
    hierarchy: state.hierarchy
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(Hierarchy);
