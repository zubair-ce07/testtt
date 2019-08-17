import React, { Component } from "react";
import { Field, Form } from "react-final-form";
import { connect } from "react-redux";

import { createComment } from "../../actions/comment.action";

import "./AddComment.sass";

class AddComment extends Component {
  state = {};

  onSubmit = formValues => {
    this.props.createComment(formValues, this.props.postId);
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

  render = () => {
    return (
      <div className="AddComment">
        <div className="card">
          <div className="prompt">
            <img
              className="profile-picture-small"
              src={this.props.user.displayPicture}
              alt=""
            />
            <Form onSubmit={this.onSubmit} render={this.renderForm} />
          </div>
          <span className="post-prompt">Press Enter to post.</span>
        </div>
      </div>
    );
  };
}

const mapStateToProps = ({ comments, auth }) => {
  return { comments: comments, user: auth.user };
};

export default connect(
  mapStateToProps,
  { createComment }
)(AddComment);
