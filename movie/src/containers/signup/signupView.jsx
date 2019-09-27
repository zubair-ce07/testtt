import React from "react";
import { FormField, Button, Select } from "../../components";

class SignUpView extends React.Component {
  render() {
    return (
      <form >
        <FormField
          name="first_name"
          field="First Name"
          type="text"
          icon="fa-user"
        />
        <FormField
          name="last_name"
          field="Last Name"
          type="text"
          icon="fa-user"
        />
        <Select options={["male", "female"]} />
        <Button text="SignUp" />
        
      </form>
    );
  }
}

export { SignUpView };
