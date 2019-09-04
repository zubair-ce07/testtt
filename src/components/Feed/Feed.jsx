import React, { Component } from "react";
import { connect } from "react-redux";

import { fetchFeedAndUsers } from "../../actions/post.actions";
import Post from "../Post/Post";

import "./Feed.css";

class Feed extends Component {
  state = {};

  componentDidMount = () => {
    this.props.fetchFeedAndUsers();
  };

  renderPosts = () => {
    return this.props.posts
      .sort((a, b) => a.created_at < b.created_at)
      .map(post => {
        return <Post key={post.id} post={post} />;
      });
  };

  render = () => {
    return <>{this.renderPosts()}</>;
  };
}

const mapStateToProps = state => {
  return { posts: Object.values(state.posts) };
};

export default connect(
  mapStateToProps,
  { fetchFeedAndUsers }
)(Feed);
