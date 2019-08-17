import React, { Component } from "react";
import { Field, Form } from "react-final-form";
import { connect } from "react-redux";

import { createPost } from "../../actions/post.action";

import "./NewPost.css";

class NewPost extends Component {
  state = {};

  onSubmit = formValues => {
    this.props.createPost(formValues);
  };

  renderInput = ({ input, placeholder, meta }) => {
    return (
      <div className="NewPost">
        <div className="card">
          <div className="row">
            <div className="col-1">
              <img
                className="profile-picture"
                src={this.props.user.displayPicture}
                alt=""
              />
            </div>
            <div className="col-11">
              <input
                className="form-control"
                {...input}
                type={input.type}
                placeholder={placeholder}
              />
            </div>
          </div>
          <hr />
          <span className="post-prompt">Press Enter to post.</span>
        </div>
        <div />
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
          name="status"
          placeholder="What's on your mind?"
          type="text"
          component={this.renderInput}
        />
      </form>
    );
  };

  validate = formValues => {
    const errors = {};

    if (!formValues.status) errors.status = "Cannot create empty post!";

    return errors;
  };

  render = () => {
    return (
      <div>
        <Form
          onSubmit={this.onSubmit}
          validate={this.validate}
          render={this.renderForm}
        />
      </div>
    );
  };
}

const mapStateToProps = state => {
  return { user: state.auth.user };
};

export default connect(
  mapStateToProps,
  { createPost }
)(NewPost);
