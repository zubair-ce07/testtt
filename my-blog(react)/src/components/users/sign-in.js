import React, { Component } from 'react';
// import { Link } from 'react-router-dom';

import {
  Button, Form, FormGroup, Label, Input, Row, Col, FormFeedback
} from 'reactstrap';

import UserService from './service';

class SignIn extends Component {
  constructor(props) {
    super(props);

    this.state = {
      invalid: false
    };

    this.service = new UserService();
    this.signIn = this.signIn.bind(this);
  }

  async signIn(event) {
    event.preventDefault();
    const form = event.target;
    const credentials = {
      username: form.username.value,
      password: form.password.value
    };

    const response = await this.service.login(credentials);
    if (response.success) {
      this.props.history.push('/blogs');
    } else {
      this.setState({ invalid: true });
    }
  }

  render() {
    const { invalid } = this.state;
    return (
      <Row>
        <Col sm="12" md={{ size: 4, offset: 4 }}>
          <Form onSubmit={this.signIn}>
            <h2>Sign In</h2>
            <FormGroup>
              <Label for='username' hidden>Username</Label>
              <Input
                type='text'
                name='username'
                id='username'
                placeholder='Username'
                required
                invalid={invalid}
              />
            </FormGroup>
            <FormGroup>
              <Label for='password' hidden>Password</Label>
              <Input
                type='password'
                name='password'
                id='password'
                placeholder='Password'
                required
                invalid={invalid}
              />
              <FormFeedback>
                Username or password is incorrect
              </FormFeedback>
            </FormGroup>
            <Button block>Sign In</Button>
            <br />
          </Form>
        </Col>
      </Row>
    );
  }
}

export default SignIn;
