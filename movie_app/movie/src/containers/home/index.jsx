import { connect } from "react-redux";
import { Home } from "./home";
import { logoutUser } from "../../actions/auth";

const mapStateToProps = ({ authReducer: { user } }) => ({
  user
});

const mapDispatchToProps = { logoutUser };

const HomeContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(Home);

export { HomeContainer };
