import { compose } from "redux";
import { connect } from "react-redux";
import { withHandlers } from "recompose";
import { logoutUser } from "../../actions/authActions";
import { withRouter } from "react-router";

const mapStateToProps = (state, ownProps) => ({
  token: state.auth.token
});

const mapDispatchToProps = dispatch => ({
  logoutUser: () => dispatch(logoutUser())
});

export default compose(
  connect(
    mapStateToProps,
    mapDispatchToProps
  ),
  withHandlers({
    handleLogout: ({ logoutUser }) => () => {
      logoutUser();
    }
  })
);
