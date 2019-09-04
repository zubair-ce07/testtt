import { compose } from "redux";
import { withHandlers } from "recompose";
import { connect } from "react-redux";
import { required } from "../../utils/formValidators";
import { loginUser } from "../../actions/authActions";

const mapStateToProps = state => ({
  isLogging: state.auth.isLogging,
  authErrors: state.auth.authErrors,
  user: state.user.data
});

const mapDispatchToProps = dispatch => ({
  loginUser: creds => dispatch(loginUser(creds))
});

export default compose(
  connect(
    mapStateToProps,
    mapDispatchToProps
  ),
  withHandlers({
    onSubmit: ({ loginUser }) => values => {
      loginUser(values);
    },
    validate: () => values => {
      const errors = {};

      // required fields
      errors.username = required(values.username);
      errors.password = required(values.password);

      return errors;
    }
  })
);
