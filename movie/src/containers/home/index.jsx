import { connect } from "react-redux";
import { Home } from "./home";
import { logoutUser } from "../../actions/auth";

const mapStateToProps = state => ({
  user: state.authReducer.user
});

const HomeContainer = connect(
  mapStateToProps,
  { logoutUser }
)(Home);

export { HomeContainer };
