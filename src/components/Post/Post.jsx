import React, { Component } from "react";
import { connect } from "react-redux";
import moment from "moment";

import history from "../../history";
import AddComment from "../AddComment/AddComment";
import CommentList from "../CommentList/CommentList";

import { deletePost } from "../../actions/post.action";

import "./Post.sass";

class Post extends Component {
  state = { showComments: false, description: "View comments" };

  toggleComments = () => {
    this.setState({
      showComments: !this.state.showComments,
      description: this.state.showComments ? "View comments" : "Hide comments"
    });
  };

  renderComments = () => {
    if (this.state.showComments)
      return <CommentList postId={this.props.post.id} />;
  };

  handleDeletePost = postId => {
    this.props.deletePost(postId);
  };

  renderUserName = userId => {
    const user = this.props.users[userId];
    if (user) {
      return `${user.firstName} ${user.lastName}`;
    }
    return "...";
  };

  renderUserPicture = userId => {
    const user = this.props.users[userId];
    if (user) {
      return (
        <img className="profile-picture" src={user.displayPicture} alt="" />
      );
    }
    return "...";
  };

  renderDate(date) {
    if (
      moment(date)
        .add(3, "hours")
        .isBefore()
    )
      return moment(date).calendar(null, {
        lastWeek: "MMMM D [at] h[:]m A"
      });
    else return moment(date).fromNow();
  }

  renderAddComment = postId => {
    if (this.props.isSignedIn) return <AddComment postId={postId} />;
  };

  renderPost = post => {
    return (
      <div className="Post">
        <div className="card">
          <button
            onClick={() => this.handleDeletePost(post.id)}
            type="button"
            className="close"
          >
            <span aria-hidden="true">&times;</span>
          </button>
          <div className="meta">
            <div>{this.renderUserPicture(post.author)}</div>
            <div className="name-time">
              <div
                onClick={() => history.push(`/user/${post.id}`)}
                className="profile-link"
              >
                {this.renderUserName(post.author)}
              </div>
              <div className="time">{this.renderDate(post.time)}</div>
            </div>
          </div>
          <div className="post-status">{post.status}</div>
          <div className="comments-toggle">
            <div onClick={this.toggleComments}>{this.state.description}</div>
          </div>
        </div>
        {this.renderComments()}
        {this.renderAddComment(post.id)}
      </div>
    );
  };

  render = () => {
    return this.renderPost(this.props.post);
  };
}

const mapStateToProps = state => {
  return { users: state.users, isSignedIn: state.auth.isSignedIn };
};

export default connect(
  mapStateToProps,
  { deletePost }
)(Post);
