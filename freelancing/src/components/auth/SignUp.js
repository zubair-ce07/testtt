import React from 'react'
import enhance from './SignUp.enhancer'
import { Form, Field } from 'react-final-form'
import createDecorator from 'final-form-focus'

import { StyledForm, FormTitle, Wrapper, FormRow, FormInput, FormButton, FormErrorText, FormErrorRow } from './styles';

const renderInput = ({ input, meta, ...restProps }) => (
    <React.Fragment>
        <FormInput {...input} {...restProps} error={meta.error && meta.touched} />
        {meta.error && meta.touched &&
            <FormErrorText>{meta.error}</FormErrorText>}
    </React.Fragment>
)

const focusOnError = createDecorator()

const SignUp = ({ onSubmit, validate }) => {
    return (
        <Wrapper>
            <Form
                onSubmit={onSubmit}
                validate={validate}
                decorators={[focusOnError]}
                render={({ handleSubmit, submitting, errors }) => (
                    <StyledForm onSubmit={handleSubmit}>
                        <FormTitle>Join Fiverr</FormTitle>
                        <FormErrorRow>
                            <Field component={renderInput} name="username" type="text" placeholder="Username" />
                        </FormErrorRow>
                        <FormErrorRow>
                            <Field component={renderInput} name="firstname" type="text" placeholder="First Name" />
                        </FormErrorRow>
                        <FormErrorRow>
                            <Field component={renderInput} name="lastname" type="text" placeholder="Last Name" />
                        </FormErrorRow>
                        <FormErrorRow>
                            <Field component={renderInput} name="email" type="email" placeholder="martin@example.com" />
                        </FormErrorRow>
                        <FormErrorRow>
                            <Field component={renderInput} name="password" type="password" placeholder="Password" />
                        </FormErrorRow>
                        <FormErrorRow>
                            <Field component={renderInput} name="password2" type="password" placeholder="Confirm Password" />
                        </FormErrorRow>
                        <FormRow>
                            <FormButton type="submit" disabled={submitting}>Register Me</FormButton>
                        </FormRow>
                    </StyledForm>
                )}
            />
        </Wrapper>
    )
}

export default enhance(SignUp)
