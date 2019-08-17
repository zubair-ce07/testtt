import React, { Component } from "react";
import { Field, Form } from "react-final-form";
import { connect } from "react-redux";

import { createComment } from "../../actions/comment.action";

class AddComment extends Component {
  state = {};

  onSubmit = formValues => {
    this.props.createComment(formValues, this.props.postId);
  };

  renderInput = ({ input, placeholder, meta, type }) => {
    return (
      <div className="add-comment-card card">
        <div className="row">
          <div className="col-1">
            <img
              className="profile-picture-small"
              src={this.props.user.displayPicture}
              alt=""
            />
          </div>
          <div className="col-11">
            <input
              {...input}
              type={type}
              className="form-control"
              placeholder={placeholder}
            />
          </div>
          <hr />
          <span className="post-prompt">Press Enter to post.</span>
        </div>
      </div>
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
    return <Form onSubmit={this.onSubmit} render={this.renderForm} />;
  };
}

const mapStateToProps = ({ comments, auth }) => {
  return { comments: comments, user: auth.user };
};

export default connect(
  mapStateToProps,
  { createComment }
)(AddComment);
