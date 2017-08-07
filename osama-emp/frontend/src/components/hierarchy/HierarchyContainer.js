import { connect } from "react-redux";
import Hierarchy from "./Hierarchy";
import { replaceDirects } from "../../actions";

function mapDispatchToProps(dispatch) {
  return {
    onClick: username => {
      dispatch(replaceDirects(username));
    }
  };
}

function mapStateToProps(state) {
  return {
    hierarchy: state.hierarchy
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(Hierarchy);
