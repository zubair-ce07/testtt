import { compose } from "redux";
import { withHandlers } from "recompose";
import { required } from "../../utils/formValidators";

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

      return errors;
    }
  })
);
