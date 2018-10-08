import React, { Component } from 'react';

import { Button, Form, Row, Col } from 'reactstrap';

import InputField from './input-field';
import container from './container';

class SignUp extends Component {
  constructor(props) {
    super(props);

    this.updateValue = this.updateValue.bind(this);
    this.submit = this.submit.bind(this);
    this.matchPassword = this.matchPassword.bind(this);

    if (props.user.id) {
      this.title = 'Profile';
      this.buttonText = 'Update';
      this.updating = true;
    } else {
      this.title = this.buttonText = 'Sign Up';
    }
  }

  componentDidMount() {
    const { history, match } = this.props;

    if (this.updating && match.path.includes('signup')) {
      history.push('/');
    }
  }

  updateValue(event) {
    const { name, value, required } = event.target;
    this.props.updateField(name, value, required);
  }

  submit(event) {
    event.preventDefault();
    this.props.saveUser();
  }

  matchPassword() {
    this.props.matchPassword();
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
    } = this.props.user;

    return (
      <Row>
        <Col sm="12" md={{ size: 6, offset: 3 }}>
          <Form onSubmit={this.submit}>
            <h2>{this.title}</h2>
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
              readOnly={this.updating}
            />
            <InputField
              title='Password'
              name='password'
              type='password'
              placeholder={this.updating ? '(Unchanged)' : 'Password'}
              value={password}
              validator={this.matchPassword}
              errors={errors['password']}
              onChange={this.updateValue}
              required={!this.updating}
            />
            <InputField
              title='Confirm Password'
              name='confirm_password'
              type='password'
              placeholder={this.updating ? '(Unchanged)' : 'Confirm Password'}
              value={confirm_password}
              validator={this.matchPassword}
              errors={errors['confirm_password']}
              onChange={this.updateValue}
              required={!this.updating || Boolean(password)}
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
                <Button block>{this.buttonText}</Button>
              </Col>
            </Row>
            <br />
          </Form>
        </Col>
      </Row>
    );
  }
}

export default container(SignUp);
