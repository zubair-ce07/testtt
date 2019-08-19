import React, { Component } from "react";
import { connect } from "react-redux";
import { fetchUserPosts } from "../../actions/post.action";
import Post from "../Post/Post";

import "./UserWall.sass";

class UserWall extends Component {
  state = {};

  componentDidMount = () => {
    this.props.fetchUserPosts(this.props.userId);
  };

  renderPosts = () => {
    return this.props.posts.map(post => {
      return <Post key={post.id} post={post} />;
    });
  };

  render = () => {
    return <div className="main">{this.renderPosts()}</div>;
  };
}

const mapStateToProps = state => {
  return { posts: Object.values(state.posts) };
};

export default connect(
  mapStateToProps,
  { fetchUserPosts }
)(UserWall);
