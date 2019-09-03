import React, { Component } from "react";
import { Field, Form } from "react-final-form";
import { connect } from "react-redux";

import { createPost } from "../../actions/post.actions";
import { fetchUser } from "../../actions/user.actions";
import MediaUpload from "../MediaUpload/MediaUpload";

import "./NewPost.sass";

class NewPost extends Component {
  state = {};

  componentDidMount = () => {
    fetchUser(this.props.user_id);
  };

  onSubmit = formValues => {
    this.props.createPost(formValues, this.state.media);
    this.setState({});
  };

  handleMediaAdd = media => {
    this.setState({ media });
  };

  renderInput = ({ input, placeholder, meta }) => {
    return (
      <>
        <input
          className="form-control"
          {...input}
          type={input.type}
          placeholder={placeholder}
        />
      </>
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
    const { user_id, users } = this.props;
    const user = users[user_id];
    if (user)
      return (
        <div className="NewPost">
          <div className="card">
            <div className="prompt">
              <img
                className="profile-picture"
                src={user.display_picture}
                alt=""
              />
              <Form
                onSubmit={this.onSubmit}
                validate={this.validate}
                render={this.renderForm}
              />
            </div>
            <hr />
            {/* <span className="post-prompt">Press Enter to post.</span> */}
            <MediaUpload onMediaChange={this.handleMediaAdd}></MediaUpload>
          </div>
        </div>
      );

    return "...";
  };
}

const mapStateToProps = state => {
  return { user_id: state.auth.user_id, users: state.users };
};

export default connect(
  mapStateToProps,
  { createPost }
)(NewPost);
