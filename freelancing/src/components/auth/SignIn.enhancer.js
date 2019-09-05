import { compose } from "redux";
import { withHandlers } from "recompose";
import { connect } from "react-redux";
import { required } from "../../utils/formValidators";
import { loginUser } from "../../actions/authActions";
import withAuthorization from "../../hoc/withAuthorization";
import { ROUTES } from "../../constants/routes";
import { withRouter } from "react-router";

const mapStateToProps = state => ({
  isLogging: state.auth.isLogging,
  authErrors: state.auth.authErrors,
  user: state.user.data
});

const mapDispatchToProps = dispatch => ({
  loginUser: (creds, history) => dispatch(loginUser(creds, history))
});

const condition = token => token === null;

export default compose(
  withRouter,
  withAuthorization(condition, ROUTES.ROOT),
  connect(
    mapStateToProps,
    mapDispatchToProps
  ),
  withHandlers({
    onSubmit: ({ loginUser, history }) => values => {
      loginUser(values, history);
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
