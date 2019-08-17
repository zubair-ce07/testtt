import React, { Component } from "react";
import { connect } from "react-redux";
import moment from "moment";

import AddComment from "../AddComment/AddComment";
import CommentList from "../CommentList/CommentList";

import { deletePost } from "../../actions/post.action";

import "./Post.css";

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

  /*
    TODO: Move styles to stylesheel
  */
  closeButtonStyles = {
    position: "absolute",
    right: "14px",
    top: "10px"
  };

  handleDeletePost = postId => {
    this.props.deletePost(postId);
  };

  renderUserDetails = userId => {
    const user = this.props.users[userId];
    if (user) {
      return (
        <div className="row">
          <div className="col-1">
            <img className="profile-picture" src={user.displayPicture} alt="" />
          </div>
          <div className="col-11">
            <span className="profile-link">
              {user.firstName} {user.lastName}
            </span>
          </div>
        </div>
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
      <>
        <div className="post-card card">
          <button
            onClick={() => this.handleDeletePost(post.id)}
            type="button"
            style={this.closeButtonStyles}
            className="close"
          >
            <span aria-hidden="true">&times;</span>
          </button>
          <div className="card-body">
            {this.renderUserDetails(post.author)}
            <span className="post-time">{this.renderDate(post.time)}</span>
            <div className="post-status">{post.status}</div>
          </div>
          <span className="comments-count" onClick={this.toggleComments}>
            {this.state.description}
          </span>
        </div>
        {this.renderComments()}
        {this.renderAddComment(post.id)}
      </>
    );
  };

  render = () => {
    return <div>{this.renderPost(this.props.post)}</div>;
  };
}

const mapStateToProps = state => {
  return { users: state.users, isSignedIn: state.auth.isSignedIn };
};

export default connect(
  mapStateToProps,
  { deletePost }
)(Post);
