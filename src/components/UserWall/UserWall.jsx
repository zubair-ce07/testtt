import React, { Component } from "react";
import { connect } from "react-redux";
import { fetchUserPosts } from "../../actions/post.actions";
import Post from "../Post/Post";

import "./UserWall.sass";

class UserWall extends Component {
  state = {};

  componentDidMount = () => {
    this.props.fetchUserPosts(this.props.id);
  };

  componentDidUpdate = () => {
    this.props.fetchUserPosts(this.props.id);
  };

  renderPosts = () => {
    return this.props.posts
      .sort((a, b) => a.created_at < b.created_at)
      .map(post => {
        return <Post key={post.id} post={post} />;
      });
  };

  render = () => {
    return <div className="main">{this.renderPosts()}</div>;
  };
}

const mapStateToProps = (state, { user_id }) => {
  return { posts: Object.values(state.posts), id: user_id };
};

export default connect(
  mapStateToProps,
  { fetchUserPosts }
)(UserWall);
