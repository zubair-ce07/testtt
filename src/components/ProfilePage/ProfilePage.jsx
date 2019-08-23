import React, { Component } from "react";
import { connect } from "react-redux";
import { fetchUser } from "../../actions/user.actions";
import UserWall from "../UserWall/UserWall";
import Topbar from "../Topbar/Topbar";

import "./ProfilePage.sass";

class ProfilePage extends Component {
  componentDidMount = () => {
    const { fetchUser } = this.props;
    const { id } = this.props.match.params;
    fetchUser(id);
  };

  renderUserDetails = () => {
    const { user } = this.props;
    if (user) {
      return (
        <>
          <Topbar title={` ${user.firstName}'s Profile`} />
          <div className="user-card">
            <div className="card">
              <img className="card-img-top" src={user.displayPicture} alt="" />
              <div className="card-body">
                <h5 className="card-title">
                  {user.firstName} {user.lastName}
                </h5>
                <p className="card-text">{user.email}</p>
              </div>
              <ul className="list-group list-group-flush">
                <li className="list-group-item">Software Engineer</li>
                <li className="list-group-item">2nd December 1997</li>
                <li className="list-group-item">From Lahore</li>
              </ul>
            </div>
          </div>
          <UserWall userId={user.id} />
        </>
      );
    } else return <h1>Loading</h1>;
  };

  render = () => {
    return this.renderUserDetails();
  };
}

const mapStateToProps = (state, ownProps) => {
  const { id } = ownProps.match.params;
  return { user: state.users[id] };
};

export default connect(
  mapStateToProps,
  { fetchUser }
)(ProfilePage);
