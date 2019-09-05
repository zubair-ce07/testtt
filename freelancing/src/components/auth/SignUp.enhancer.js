import { compose } from "redux";
import { withHandlers } from "recompose";
import {
  required,
  isValidEmail,
  isPasswordMatch,
  minLength
} from "../../utils/formValidators";
import withAuthorization from "../../hoc/withAuthorization";
import { ROUTES } from "../../constants/routes";
import { withRouter } from "react-router";
import { connect } from "react-redux";
import { registerUser } from "../../actions/authActions";

const mapStateToProps = state => ({
  isLogging: state.auth.isLogging,
  authErrors: state.auth.authErrors,
  user: state.user.data
});

const mapDispatchToProps = dispatch => ({
  registerUser: (user, history) => dispatch(registerUser(user, history))
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
    onSubmit: ({ registerUser, history }) => values => {
      const { password2, firstname, lastname, ...user } = values;
      registerUser(
        { first_name: firstname, last_name: lastname, ...user },
        history
      );
    },
    validate: () => values => {
      const errors = {};

      // required fields
      errors.username = required(values.username);
      errors.password = required(values.password);
      errors.password2 = required(values.password2);
      errors.firstname = required(values.firstname);
      errors.lastname = required(values.lastname);
      errors.email = required(values.email);

      // valid email
      if (!isValidEmail(values.email)) errors.email = "invalid email address.";
      // password matches
      if (!isPasswordMatch(values.password, values.password2))
        errors.password2 = "password did not match";
      // password min length
      errors.password = !!values.password && minLength(6)(values.password);

      return errors;
    }
  })
);
