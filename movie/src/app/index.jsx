import { connect } from "react-redux";
import { App } from "./app";

const mapStateToProps = state => ({
  isAuthenticated: state.authReducer.isAuthenticated
});
const AppContainer = connect(mapStateToProps)(App);

export { AppContainer };
