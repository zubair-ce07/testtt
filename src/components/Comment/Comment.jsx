import React, { Component } from "react";
import { connect } from "react-redux";

import "./Comment.css";

class Comment extends Component {
  state = {};

  render = () => {
    const author = this.props.comment.author;
    return (
      <div>
        <div className="comment-card card">
          <div className="row no-gutters">
            <div className="col-1">
              <img
                className="profile-picture-small"
                src={this.props.users[author].displayPicture}
                alt=""
              />
            </div>
            <div className="col-md-auto message">
              <span className="profile-link">
                {this.props.users[author].firstName}
              </span>
              <span>{this.props.comment.message}</span>
            </div>
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
