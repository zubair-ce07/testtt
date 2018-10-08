import React, { Component, Fragment } from 'react';
import { Link } from 'react-router-dom';

import { Button, Form, Media, Modal, ModalHeader, ModalBody, ModalFooter } from 'reactstrap';
import TextareaAutosize from 'react-textarea-autosize';
import moment from 'moment';

import Tag from './tag';
import BlogsService from './blogs.service';
import CommentsService from './comments.service';

import userContainer from '../users/container';

class Blog extends Component {
  constructor(props) {
    super(props);

    this.state = {
      id: 0,
      title: '',
      body: '',
      tags: [],
      replyTo: 0,
      comments: [],
    };

    this.id = +this.props.match.params.id;
    this.blogsService = new BlogsService();
    this.commentsService = new CommentsService();

    this.addComment = this.addComment.bind(this);
    this.reply = this.reply.bind(this);
    this.cancelReply = this.cancelReply.bind(this);
    this.addReply = this.addReply.bind(this);
  }

  async componentDidMount() {
    if (!this.id) {
      this.props.history.push('/404');
      return;
    }

    const response = await this.blogsService.getById(this.id);

    if (response.success) {
      this.setState({ ...response.data });
    } else {
      this.props.history.push('/404');
    }
  }

  async addComment(event) {
    event.preventDefault();
    const comment = event.target.comment;
    const body = comment.value;
    const response = await this.commentsService.add({
      body,
      object_id: this.id,
      content_type: 8, // blog content type
    });

    if (response.success) {
      comment.value = '';
      const { comments } = this.state;
      comments.push(response.data);
      this.setState({ comments });
    }
  }

  reply(event) {
    const replyTo = +event.target.dataset.commentId;
    this.setState({ replyTo });
  }

  cancelReply(event) {
    event.preventDefault();
    this.setState({ replyTo: 0 });
  }

  async addReply(event) {
    event.preventDefault();
    let { comments, replyTo } = this.state;
    const body = event.target.comment.value;
    const responsePromise = this.commentsService.add({
      body,
      object_id: replyTo,
      content_type: 10, // comment content type
    });

    const comment = this.findComment(comments, replyTo);

    const response = await responsePromise;

    if (response.success && comment) {
      replyTo = 0;
      comment.comments.push(response.data);
    }
    this.setState({ comments, replyTo });
  }

  findComment(comments, id) {
    if (comments) {
      for (let i = 0; i < comments.length; i++) {
        if (comments[i].id === id) {
          return comments[i];
        }
        let found = this.findComment(comments[i].comments, id);
        if (found) return found;
      }
    }
  }

  renderComments(comments, level = 0) {
    return comments.map(comment => this.renderComment(comment, level));
  }

  renderComment({ id, writer, body, created_at, comments }, level) {
    const isSignedIn = Boolean(this.props.user.id);
    return (
      <Media key={id}>
        <Media body>
          <Media heading>{writer}</Media>
          <small>{moment(created_at).fromNow()}</small><br />
          {body}<br />
          {isSignedIn && level < 4 &&
            <Button color="link" data-comment-id={id} onClick={this.reply}>
              reply
            </Button>
          }
          {this.renderComments(comments, level + 1)}
        </Media>
      </Media>
    );
  }

  render() {
    const { id, title, body, tags, writer, comments, replyTo } = this.state;
    const { id: userId, first_name, last_name } = this.props.user;
    return (
      <Fragment>
        {this.props.user.id === writer &&
          <Button
            tag={Link}
            to={`/blogs/edit/${id}`}
            color='primary'
            className='edit-button'
          >
            Edit
          </Button>
        }
        <h2>{title}</h2>
        <p>
          {body} <br />
          {tags.map(tag => <Tag key={tag.id} name={tag.name} />)}
        </p>
        <h3>Comments:</h3>
        {this.renderComments(comments)}

        {Boolean(userId) &&
          <Media>
            <Media body>
              <Media heading>
                {first_name} {last_name}
              </Media>
              <Form onSubmit={this.addComment}>
                <TextareaAutosize
                  className='form-control'
                  minRows={2}
                  name='comment'
                  required
                />
                <br />
                <Button>Comment</Button>
              </Form>
            </Media>
          </Media>
        }


        <Modal isOpen={Boolean(replyTo)}>
          <ModalHeader>Add a reply</ModalHeader>
          <Form onSubmit={this.addReply}>
            <ModalBody>
              <TextareaAutosize
                name='comment'
                required
                className='form-control'
                minRows={3}
                autoFocus
              />
            </ModalBody>
            <ModalFooter>
              <Button color="primary">Add</Button>{' '}
              <Button color="secondary" onClick={this.cancelReply}>
                Cancel
              </Button>
            </ModalFooter>
          </Form>
        </Modal>
      </Fragment>
    );
  }
}

export default userContainer(Blog);
