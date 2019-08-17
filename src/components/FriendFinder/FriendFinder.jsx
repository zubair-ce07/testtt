import React, { Component } from "react";
import { connect } from "react-redux";
import {
  fetchAllUsers,
  followUser,
  unfollowUser
} from "../../actions/user.action";

import "./FriendFinder.css";

class FriendFinder extends Component {
  componentDidMount = () => {
    this.props.fetchAllUsers();
  };

  follow = userId => {
    this.props.followUser(userId);
  };

  unfollow = userId => {
    this.props.unfollowUser(userId);
  };

  renderFollow = (userId, myId) => {
    const me = this.props.users[myId];
    if (me.following[userId])
      return <button onClick={() => this.unfollow(userId)}>Unfollow</button>;
    return <button onClick={() => this.follow(userId)}>Follow</button>;
  };

  renderUsers = () => {
    const { users, me } = this.props;
    if (users) {
      return Object.keys(users).map(userId => {
        /**
         * TODO: Investigate => Check not working.
         */
        if (userId !== me.id) {
          return (
            <div key={userId}>
              <img src={users[userId].displayPicture} alt="" />
              {users[userId].firstName} {users[userId].lastName}
              {this.renderFollow(userId, me.id)}
            </div>
          );
        }
        return <></>;
      });
    } else {
      return <div>LOADING</div>;
    }
  };
  render = () => {
    return <div>{this.renderUsers()}</div>;
  };
}

const mapStateToProps = state => {
  return { users: state.users, me: state.auth.user };
};

export default connect(
  mapStateToProps,
  { fetchAllUsers, followUser, unfollowUser }
)(FriendFinder);
