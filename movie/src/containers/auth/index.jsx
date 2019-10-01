import { connect } from "react-redux";
import { Auth } from "./auth";
import { loginUser, registerUser } from "../../actions/auth";
import { updateUser } from "../../actions/user";
import { loginForm } from "../../actions/form";

const mapStateToProps = state => ({
  user: state.authReducer.user,
  isLoginForm: state.formReducer.isLoginForm,
  error: state.authReducer.error,
  isAuthenticated: state.authReducer.isAuthenticated
});
const AuthContainer = connect(
  mapStateToProps,
  { loginUser, updateUser, loginForm, registerUser }
)(Auth);

export { AuthContainer };
