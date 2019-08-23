import React, { Component } from "react";
import { connect } from "react-redux";

import Comment from "../Comment/Comment";
import { fetchCommentsAndUsers } from "../../actions/comment.actions";

import "./CommentList.sass";

class CommentList extends Component {
  state = {};

  componentDidMount = () => {
    this.props.fetchCommentsAndUsers(this.props.postId);
  };

  renderComments = () => {
    if (this.props.comments === undefined) return <small>Loading</small>;
    if (this.props.comments.length) {
      return this.props.comments.map(comment => {
        return <Comment key={comment.id} comment={comment} />;
      });
    } else {
      return <small>No comments added so far</small>;
    }
  };

  render = () => {
    return (
      <div className="CommentList">
        <div className="card">{this.renderComments()}</div>
      </div>
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
