import React, { Component } from "react";
import { connect } from "react-redux";

import "./Comment.sass";

class Comment extends Component {
  state = {};

  render = () => {
    const { comment, users } = this.props;
    return (
      <div className="Comment">
        <img
          className="profile-picture-small"
          src={users[comment.author].displayPicture}
          alt=""
        />
        <div className="message">
          <div>
            <span className="profile-link">
              {users[comment.author].firstName} {users[comment.author].lastName}
            </span>
            {comment.message}
          </div>
        </div>
      </div>
    );
  };
}

const mapStateToProps = state => {
  return { users: state.users };
};

export default connect(mapStateToProps)(Comment);
