import { compose } from "redux";
import { withHandlers, withState } from "recompose";
import { connect } from "react-redux";
import { required } from "../../utils/formValidators";
import { loginUser } from "../../actions/authActions";

const mapStateToProps = state => ({
  isLogging: state.auth.isLogging
});

const mapDispatchToProps = dispatch => ({
  loginUser: (creds, setSigningIn) => dispatch(loginUser(creds, setSigningIn))
});

export default compose(
  withState("signingIn", "setSigningIn", false),
  connect(
    mapStateToProps,
    mapDispatchToProps
  ),
  withHandlers({
    onSubmit: ({ loginUser, setSigningIn }) => values => {
      loginUser(values, setSigningIn);
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
