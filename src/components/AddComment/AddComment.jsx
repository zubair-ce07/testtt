import React, { Component } from "react";
import { Field, Form } from "react-final-form";
import { connect } from "react-redux";

import { createComment } from "../../actions/comment.actions";
import { fetchUser } from "../../actions/user.actions";

import "./AddComment.sass";

class AddComment extends Component {
  state = {};

  componentDidMount = () => {
    // this.props.fetchUser(this.props.auth.user_id);
  };

  onSubmit = formValues => {
    this.props.createComment(formValues, this.props.postId);
    this.props.showComments();
  };

  renderInput = ({ input, placeholder, meta, type }) => {
    return (
      <input
        {...input}
        type={type}
        className="form-control"
        placeholder={placeholder}
      />
    );
  };

  renderForm = ({ handleSubmit, form }) => {
    return (
      <form
        onSubmit={async e => {
          await handleSubmit(e);
          form.reset();
        }}
      >
        <Field
          name="message"
          type="text"
          placeholder="Add comment"
          component={this.renderInput}
        />
      </form>
    );
  };

  fetchUserImage = () => {
    const { user } = this.props;
    if (user)
      return (
        <img
          className="profile-picture-small"
          src={user.display_picture}
          alt=""
        />
      );
    else return <>Hello</>;
  };

  render = () => {
    return (
      <div className="AddComment">
        <div className="card">
          <div className="prompt">
            {this.fetchUserImage()}
            <Form onSubmit={this.onSubmit} render={this.renderForm} />
          </div>
          <span className="post-prompt">Press Enter to post.</span>
        </div>
      </div>
    );
  };
}

const mapStateToProps = ({ comments, auth, users }) => {
  return { comments: comments, user: users[auth.user_id], auth };
};

export default connect(
  mapStateToProps,
  { createComment, fetchUser }
)(AddComment);
