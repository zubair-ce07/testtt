import React, { Component } from 'react';
import { Link } from 'react-router-dom';

import { Button, Form, FormGroup, Label, Input } from 'reactstrap';
import TextareaAutosize from 'react-textarea-autosize';

import ReactTags from 'react-tag-autocomplete';


class CreateBlog extends Component {
  constructor(props) {
    super(props);

    this.id = +this.props.match.params.id;
    this.action = props.match.path.includes('edit') ? 'Update' : 'Create';
  }

  componentDidMount() {
    if (this.props.match.path.includes('edit')) {
      if (!this.id) {
        this.props.history.push('/404');
        return;
      }

      this.props.loadBlog(this.id);
    }

    this.props.loadTags();
  }

  componentWillUnmount() {
    if (this.id) {
      this.props.resetBlog();
    }
  }

  componentWillReceiveProps(nextProps) {
    if (this.props.match.path !== nextProps.match.path) {
      this.props.resetBlog();
      this.id = undefined;
      this.action = 'Create';
    }
  }

  updateValue = (event) => {
    const { name, value } = event.target;
    this.props.updateField(name, value);
  }

  submit = (event) => {
    event.preventDefault();
    this.props.saveBlog();
  }

  render() {
    const { title, body, tags } = this.props.blog;
    const { addTagToBlog, removeTagFromBlog } = this.props;
    return (
      <Form onSubmit={this.submit}>
        <h2>{this.action} Blog</h2>
        <FormGroup>
          <Label for='title'>Title</Label>
          <Input
            type='Text'
            name='title'
            id='title'
            placeholder='A Nice Blog'
            value={title}
            onChange={this.updateValue}
            required
          />
        </FormGroup>
        <FormGroup>
          <Label for="body">Body</Label>
          <TextareaAutosize
            className='form-control'
            minRows={4}
            name="body"
            id="body"
            value={body}
            onChange={this.updateValue}
            required
          />
        </FormGroup>
        <ReactTags
          tags={tags}
          suggestions={this.props.tags}
          handleDelete={removeTagFromBlog}
          handleAddition={addTagToBlog}
          allowNew
        />
        <br />
        <Button color='primary'>{this.action}</Button>{' '}
        {Boolean(this.id) &&
          <Button
            tag={Link}
            to={`/blogs/${this.id}`}
            color='danger'
          >
            Cancel
          </Button>
        }
      </Form>
    );
  }
}

export default CreateBlog;
