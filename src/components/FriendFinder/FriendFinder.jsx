import React, { Component } from "react";
import { connect } from "react-redux";
import {
  fetchAllUsers,
  followUser,
  unfollowUser
} from "../../actions/user.action";

import "./FriendFinder.sass";

class FriendFinder extends Component {
  state = { filterString: "" };

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
    const classes = "btn btn-light ";
    const followingCss = `${classes} following`;
    const notFollowingCss = `${classes} not-following`;
    if (me.following[userId]) {
      return (
        <button className={followingCss} onClick={() => this.unfollow(userId)}>
          Unfollow
        </button>
      );
    }
    return (
      <button className={notFollowingCss} onClick={() => this.follow(userId)}>
        Follow
      </button>
    );
  };

  renderUsers = () => {
    const { users, me } = this.props;
    if (users) {
      return Object.keys(users)
        .filter(userId => {
          const name = users[userId].firstName + users[userId].lastName;
          return name
            .toLowerCase()
            .includes(this.state.filterString.toLocaleLowerCase());
        })
        .filter(userId => {
          return !(parseInt(userId) === me.id);
        })
        .map(userId => {
          return (
            <div className="contact" key={userId}>
              <img
                className="profile-picture"
                src={users[userId].displayPicture}
                alt=""
              />
              <span>
                {users[userId].firstName} {users[userId].lastName}
              </span>
              {this.renderFollow(userId, me.id)}
            </div>
          );
        });
    } else {
      return <div>LOADING</div>;
    }
  };

  filterContacts = e => {
    this.setState({ filterString: e.target.value });
  };

  render = () => {
    return (
      <div className="FriendFider">
        <div className="directory">
          <div className="title">Directory</div>
          {this.renderUsers()}
        </div>
        <div className="search">
          <i className="fa fa-search" />
          <input
            placeholder="Search contacts.."
            onChange={this.filterContacts}
          />
        </div>
      </div>
    );
  };
}

const mapStateToProps = state => {
  return { users: state.users, me: state.auth.user };
};

export default connect(
  mapStateToProps,
  { fetchAllUsers, followUser, unfollowUser }
)(FriendFinder);
