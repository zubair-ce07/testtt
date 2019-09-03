import { compose } from "redux";
import { withHandlers } from "recompose";
import {
  required,
  isValidEmail,
  isPasswordMatch,
  minLength
} from "../../utils/formValidators";

export default compose(
  withHandlers({
    onSubmit: () => values => {
      console.log(values);
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
