import React from "react";

import Form from "react-bootstrap/Form";
import Button from 'react-bootstrap/Button'
import Card from "react-bootstrap/Card";
import Container from "react-bootstrap/Container";

export const LoginForm = ({ submitForm }) => (
    <Container>
    <Card style={{ width: "50rem" }}>
      <Card.Body>
        <Form onSubmit={submitForm}>
          <Form.Group controlId="username">
            <Form.Label>User Name</Form.Label>
            <Form.Control type="text" placeholder="Enter user name" />
            <Form.Text className="text-muted">
              {/* {to show errors} */}
            </Form.Text>
          </Form.Group>

          <Form.Group controlId="password">
            <Form.Label>Password</Form.Label>
            <Form.Control type="password" placeholder="Password" />
          </Form.Group>
          <Button variant="primary" type="submit">
            Submit
          </Button>
        </Form>
      </Card.Body>
    </Card>
  </Container>
);
