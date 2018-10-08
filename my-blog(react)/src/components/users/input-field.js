import React from 'react';
import { FormGroup, Label, Input, Col, FormFeedback } from 'reactstrap';

const InputField = ({ title, name, type, value, errors, onChange, validator, placeholder, required, readOnly }) => (
  <FormGroup row>
    <Label for={name} sm={4}>{title}</Label>
    <Col sm={8}>
      <Input
        type={type}
        onChange={onChange}
        value={value}
        name={name}
        id={name}
        placeholder={placeholder || title}
        onBlur={validator}
        invalid={Boolean(errors && errors.length)}
        required={!(required === false)}
        readOnly={Boolean(readOnly)}
      />
      {
        errors && errors.map((error, index) =>
          <FormFeedback key={index}>{error}</FormFeedback>
        )
      }
    </Col>
  </FormGroup>
);

export default InputField;
