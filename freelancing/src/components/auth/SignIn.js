import React from "react";
import enhance from "./SignIn.enhancer";
import { Form, Field } from "react-final-form";
import createDecorator from "final-form-focus";
import {
  StyledForm,
  FormTitle,
  Wrapper,
  FormRow,
  FormInput,
  FormButton,
  FormErrorText,
  FormErrorRow
} from "./styles";

const renderInput = ({ input, meta, ...restProps }) => (
  <React.Fragment>
    <FormInput {...input} {...restProps} error={meta.error && meta.touched} />
    {meta.error && meta.touched && <FormErrorText>{meta.error}</FormErrorText>}
  </React.Fragment>
);

const focusOnError = createDecorator();

const SignUp = ({ onSubmit, validate, title }) => {
  return (
    <Wrapper>
      <Form
        onSubmit={onSubmit}
        validate={validate}
        decorators={[focusOnError]}
        render={({ handleSubmit, submitting }) => (
          <StyledForm onSubmit={handleSubmit}>
            <FormTitle>{title}</FormTitle>
            <FormErrorRow>
              <Field
                component={renderInput}
                name="username"
                type="text"
                placeholder="Username"
              />
            </FormErrorRow>
            <FormErrorRow>
              <Field
                component={renderInput}
                name="password"
                type="password"
                placeholder="Password"
              />
            </FormErrorRow>
            <FormRow>
              <FormButton type="submit" disabled={submitting}>
                Log In
              </FormButton>
            </FormRow>
          </StyledForm>
        )}
      />
    </Wrapper>
  );
};

export default enhance(SignUp);
