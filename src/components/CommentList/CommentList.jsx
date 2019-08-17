import React, { Component } from "react";
import { connect } from "react-redux";

import Comment from "../Comment/Comment";
import { fetchCommentsAndUsers } from "../../actions/comment.action";

import "./CommentList.css";

class CommentList extends Component {
  state = {};

  componentDidMount = () => {
    this.props.fetchCommentsAndUsers(this.props.postId);
  };

  renderComments = () => {
    if (this.props.comments === undefined)
      return <div className="alert alert-light">Loading</div>;
    if (this.props.comments.length) {
      return this.props.comments.map(comment => {
        return <Comment key={comment.id} comment={comment} />;
      });
    } else {
      return <div className="alert alert-light">No comments added so far</div>;
    }
  };

  render = () => {
    return (
      <div className="card comment-list-card">{this.renderComments()}</div>
    );
  };
}

const mapStateToProps = ({ comments }, { postId }) => {
  return { comments: comments[postId] };
};

export default connect(
  mapStateToProps,
  { fetchCommentsAndUsers }
)(CommentList);
