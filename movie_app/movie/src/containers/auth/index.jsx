import { connect } from "react-redux";
import { Auth } from "./auth";
import { loginUser, registerUser, authUserFailure } from "../../actions/auth";
import { updateForm } from "../../actions/form";

const mapStateToProps = ({
  authReducer: { user, error, isAuthenticated }, formReducer: {form}
}) => ({
  user,
  error,
  form,
  isAuthenticated
});

const mapDispatchToProps = {
  loginUser,
  updateForm,
  registerUser,
  authUserFailure
};

const AuthContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(Auth);

export { AuthContainer };
