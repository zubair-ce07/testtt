import React, { Component } from 'react';
// import { Link } from 'react-router-dom';

import {
  Button, Form, FormGroup, Label, Input, Row, Col, FormFeedback
} from 'reactstrap';
import { NotificationManager } from 'react-notifications';

import UserService from './service';

const InputField = ({ title, name, type, value, errors, onChange, validator }) => (
  <FormGroup row>
    <Label for={name} sm={4}>{title}</Label>
    <Col sm={8}>
      <Input
        type={type}
        onChange={onChange}
        value={value}
        name={name}
        id={name}
        placeholder={title}
        onBlur={validator}
        invalid={Boolean(errors && errors.length)}
        required
      />
      {
        errors && errors.map((error, index) =>
          <FormFeedback key={index}>{error}</FormFeedback>
        )
      }
    </Col>
  </FormGroup>
);

class SignUp extends Component {
  constructor(props) {
    super(props);

    this.state = {
      first_name: '',
      last_name: '',
      username: '',
      password: '',
      confirm_password: '',
      email: '',
      errors: {},
    };

    this.service = new UserService();
    this.updateValue = this.updateValue.bind(this);
    this.signUp = this.signUp.bind(this);
    this.matchPassword = this.matchPassword.bind(this);
  }

  updateValue(event) {
    const { name, value } = event.target;
    this.setState({ [name]: value });
  }

  async signUp(event) {
    event.preventDefault();
    const response = await this.service.register(this.state);
    if (response.success) {
      NotificationManager.success('Registered successfully');
      this.props.history.push('/users/signin');
    } else {
      this.setState({ errors: response.data });
    }
  }

  matchPassword() {
    const { errors, password, confirm_password } = this.state;
    errors.confirm_password = [];
    if (confirm_password && password !== confirm_password) {
      errors.confirm_password
        .push('Password and confirm password are not same');
    }
    this.setState({ errors });
  }

  render() {
    const {
      first_name,
      last_name,
      username,
      password,
      confirm_password,
      email,
      errors,
    } = this.state;

    return (
      <Row>
        <Col sm="12" md={{ size: 6, offset: 3 }}>
          <Form onSubmit={this.signUp}>
            <h2>Sign Up</h2>
            <InputField
              title='First Name'
              name='first_name'
              type='text'
              value={first_name}
              errors={errors['first_name']}
              onChange={this.updateValue}
            />
            <InputField
              title='Last Name'
              name='last_name'
              type='text'
              value={last_name}
              errors={errors['last_name']}
              onChange={this.updateValue}
            />
            <InputField
              title='Username'
              name='username'
              type='text'
              value={username}
              errors={errors['username']}
              onChange={this.updateValue}
            />
            <InputField
              title='Password'
              name='password'
              type='password'
              value={password}
              validator={this.matchPassword}
              errors={errors['password']}
              onChange={this.updateValue}
            />
            <InputField
              title='Confirm Password'
              name='confirm_password'
              type='password'
              value={confirm_password}
              validator={this.matchPassword}
              errors={errors['confirm_password']}
              onChange={this.updateValue}
            />
            <InputField
              title='Email'
              name='email'
              type='email'
              value={email}
              errors={errors['email']}
              onChange={this.updateValue}
            />
            <br />
            <Row>
              <Col sm="12" md={{ size: 8, offset: 2 }}>
                <Button block>Sign Up</Button>
              </Col>
            </Row>
            <br />
          </Form>
        </Col>
      </Row>
    );
  }
}

export default SignUp;
