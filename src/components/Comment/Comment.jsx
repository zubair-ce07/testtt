import React, { Component } from "react";
import { connect } from "react-redux";

import history from "../../history";
import "./Comment.sass";
import { fetchUser } from "../../actions/user.actions";

class Comment extends Component {
  state = {};

  componentDidMount = () => {
    const { fetchUser, comment } = this.props;
    fetchUser(comment.author);
  };

  renderUserName = () => {
    const { author } = this.props;
    if (author) return author.firstName + " " + author.lastName;
    return "...";
  };

  renderUserPicture = () => {
    const { author } = this.props;
    if (author)
      return (
        <img
          className="profile-picture-small"
          src={author.displayPicture}
          alt=""
        />
      );
    return "...";
  };

  render = () => {
    const { comment } = this.props;
    return (
      <div className="Comment">
        {this.renderUserPicture()}
        <div className="message">
          <div>
            <span
              onClick={() => history.push(`/user/${comment.author}`)}
              className="profile-link"
            >
              {this.renderUserName()}
            </span>
            {comment.message}
          </div>
        </div>
      </div>
    );
  };
}

const mapStateToProps = (state, ownProps) => {
  return { author: state.users[ownProps.comment.author] };
};

export default connect(
  mapStateToProps,
  { fetchUser }
)(Comment);
