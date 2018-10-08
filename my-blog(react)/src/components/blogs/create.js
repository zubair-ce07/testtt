import React, { Component } from 'react';
import { Link } from 'react-router-dom';

import { Button, Form, FormGroup, Label, Input } from 'reactstrap';
import TextareaAutosize from 'react-textarea-autosize';
import { NotificationManager } from 'react-notifications';

import ReactTags from 'react-tag-autocomplete';

import BlogsService from './blogs.service';


class CreateBlog extends Component {
  constructor(props) {
    super(props);

    this.state = {
      title: '',
      body: '',
      tags: [],
      suggestions: [],
    };

    this.tags = [];
    this.service = new BlogsService();
    this.id = +this.props.match.params.id;

    this.updateValue = this.updateValue.bind(this);
    this.submit = this.submit.bind(this);
    this.handleAddition = this.handleAddition.bind(this);
    this.handleDelete = this.handleDelete.bind(this);

    if (props.match.path.includes('edit')) {
      this.action = 'Update';
    } else {
      this.action = 'Create';
    }
  }

  async componentDidMount() {
    if (this.props.match.path.includes('edit')) {
      if (!this.id) {
        this.props.history.push('/404');
        return;
      }

      const response = await this.service.getById(this.id);

      if (response.success) {
        this.setState({ ...response.data });
      } else {
        this.props.history.push('/404');
      }
    }

    const tagsResponse = await this.service.getTags();
    if (tagsResponse.success) {
      this.tags = tagsResponse.data;
      this.updateSuggestions();
    }
  }

  updateValue(event) {
    const { name, value } = event.target;
    this.setState({ [name]: value });
  }

  async submit(event) {
    event.preventDefault();
    let response = null;
    // eslint-disable-next-line
    const { suggestions, ...blog } = this.state;
    if (this.id) {
      response = await this.service.update(this.id, blog);
    } else {
      response = await this.service.add(blog);
    }

    if (response.success) {
      NotificationManager.success(
        `Blog ${this.action.toLocaleLowerCase()}d successfully`);
      this.props.history.push(`/blogs/${response.data.id}`);
    } else {
      this.setState({ errors: response.data });
    }
  }

  handleAddition(tag) {
    const tags = this.state.tags;
    tags.push(tag);

    this.setState({ tags }, this.updateSuggestions);
  }

  handleDelete(index) {
    const tags = this.state.tags;
    tags.splice(index, 1);
    this.setState({ tags }, this.updateSuggestions);
  }

  updateSuggestions() {
    const tags = this.state.tags;
    let suggestions = this.tags;
    if (tags.length) {
      suggestions = suggestions.filter(tag =>
        !tags.some(existing => existing === tag)
      );
    }

    this.setState({ suggestions });
  }

  render() {
    const { title, body, suggestions, tags } = this.state;
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
          suggestions={suggestions}
          handleDelete={this.handleDelete}
          handleAddition={this.handleAddition}
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
