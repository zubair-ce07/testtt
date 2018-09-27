import React from 'react';
// import { Link } from 'react-router-dom';

import { Button, Form, FormGroup, Label, Input } from 'reactstrap';

const CreateBlog = () => (
  <Form>
    <h2>Create Blog</h2>
    <FormGroup>
      <Label for='title'>Title</Label>
      <Input type='Text' name='title' id='title' placeholder='A Nice Blog' />
    </FormGroup>
    <FormGroup>
      <Label for="body">Body</Label>
      <Input type="textarea" name="body" id="body" />
    </FormGroup>
    <FormGroup>
      <Label for='tags'>Tags</Label>
      <Input type='Text' name='tags' id='tags' placeholder='Tags' />
    </FormGroup>
    <Button>Submit</Button>
  </Form>
);

export default CreateBlog;
