import { startSearchRequest } from "../../actions";
import SearchForm from "./SearchForm";
import { connect } from "react-redux";
import { bindActionCreators } from "redux";

function mapDispatchToProps(dispatch) {
  return bindActionCreators({ startSearchRequest }, dispatch);
}

export default connect(null, mapDispatchToProps)(SearchForm);
