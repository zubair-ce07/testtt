import React, { Component } from "react";
import { connect } from "react-redux";

import { fetchAllUsers } from "../../actions/user.actions";
import {
  fetchFollowing,
  followUser,
  unfollowUser
} from "../../actions/following.actions";
import history from "../../history";

import "./FriendFinder.sass";

class FriendFinder extends Component {
  state = { filterString: "" };

  componentDidMount = () => {
    this.props.fetchAllUsers();
    this.props.fetchFollowing();
  };

  follow = user_id => {
    this.props.followUser(user_id);
  };

  unfollow = user_id => {
    this.props.unfollowUser(user_id);
  };

  renderFollow = user_id => {
    const classes = "btn btn-light ";
    const followingCss = `${classes} following`;
    const notFollowingCss = `${classes} not-following`;
    const { myFollowing } = this.props;

    if (!myFollowing) return <small>loading</small>;

    if (this.props.myFollowing[user_id]) {
      return (
        <button className={followingCss} onClick={() => this.unfollow(user_id)}>
          Unfollow
        </button>
      );
    }
    return (
      <button className={notFollowingCss} onClick={() => this.follow(user_id)}>
        Follow
      </button>
    );
  };

  renderUsers = () => {
    const { users, me } = this.props;
    if (users && me) {
      return Object.keys(users)
        .filter(user_id => {
          const name = users[user_id].first_name + users[user_id].last_name;
          return name
            .toLowerCase()
            .includes(this.state.filterString.toLocaleLowerCase());
        })
        .filter(user_id => {
          return !(parseInt(user_id) === me.id);
        })
        .map(user_id => {
          return (
            <div className="contact" key={user_id}>
              <img
                className="profile-picture"
                src={users[user_id].display_picture}
                alt=""
              />
              <span onClick={() => history.push(`/user/${user_id}`)}>
                {users[user_id].first_name} {users[user_id].last_name}
              </span>
              {this.renderFollow(user_id)}
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
  const { users, auth, followings } = state;
  return {
    users,
    me: users[auth.user_id],
    myFollowing: followings[auth.user_id]
  };
};

export default connect(
  mapStateToProps,
  { fetchAllUsers, fetchFollowing, followUser, unfollowUser }
)(FriendFinder);
