import React, { Component, Fragment } from 'react';

import {
  Button, Form, Media, Modal, ModalHeader, ModalBody, ModalFooter
} from 'reactstrap';
import TextareaAutosize from 'react-textarea-autosize';
import moment from 'moment';

class Comments extends Component {
  state = { replyTo: 0 };

  async componentDidMount() {
    this.props.loadComments(this.props.blogId);
  }

  addComment = event => {
    event.preventDefault();
    const commentElement = event.target.comment;
    const comment = {
      body: commentElement.value,
      object_id: this.props.blogId,
      content_type: 8, // blog content type
    };

    this.props.addComment(comment);
    commentElement.value = '';
  }

  reply = (event) => {
    const replyTo = +event.target.dataset.commentId;
    this.setState({ replyTo });
  }

  cancelReply = (event) => {
    event.preventDefault();
    this.setState({ replyTo: 0 });
  }

  addReply = async (event) => {
    event.preventDefault();
    const replyTo = this.state.replyTo;
    const body = event.target.comment.value;
    const comment = {
      body,
      object_id: replyTo,
      content_type: 10, // comment content type
    };

    this.props.addReply(comment);
    this.setState({ replyTo: 0 });
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
    const { replyTo } = this.state;
    const {
      comments,
      user: { id: userId, first_name, last_name }
    } = this.props;
    return (
      <Fragment>
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

export default Comments;
