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
import PropTypes from "prop-types";

const renderInput = ({ input, meta, ...restProps }) => (
  <React.Fragment>
    <FormInput {...input} {...restProps} error={meta.error && meta.touched} />
    {meta.error && meta.touched && <FormErrorText>{meta.error}</FormErrorText>}
  </React.Fragment>
);

const focusOnError = createDecorator();

const SignIn = ({ signingIn, onSubmit, validate }) => {
  return (
    <Wrapper>
      <Form
        onSubmit={onSubmit}
        validate={validate}
        decorators={[focusOnError]}
        render={({ handleSubmit, submitting }) => (
          <StyledForm onSubmit={handleSubmit}>
            <FormTitle>Login To Fiverr</FormTitle>
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
              {!signingIn ? (
                <FormButton type="submit" disabled={submitting}>
                  Log In
                </FormButton>
              ) : null}
            </FormRow>
          </StyledForm>
        )}
      />
    </Wrapper>
  );
};

SignIn.propTypes = {
  signingIn: PropTypes.bool.isRequired,
  onSubmit: PropTypes.func.isRequired,
  validate: PropTypes.func.isRequired
};

export default enhance(SignIn);
