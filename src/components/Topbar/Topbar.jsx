import React, { Component } from "react";
import { connect } from "react-redux";

import history from "../../history";
import { logout } from "../../actions/user.action";

import "./Topbar.sass";

class Topbar extends Component {
  state = {};

  renderLogButton = () => {
    if (this.props.auth.isSignedIn)
      return (
        <button className="btn btn-light" onClick={this.props.logout}>
          Log out
        </button>
      );

    return (
      <button className="btn btn-light" onClick={() => history.push("/login")}>
        Log in
      </button>
    );
  };

  render = () => {
    return (
      <div className="Topbar">
        <div className="title">{this.props.title}</div>
        {this.renderLogButton()}
      </div>
    );
  };
}

const mapStateToProps = state => {
  return { auth: state.auth };
};

export default connect(
  mapStateToProps,
  { logout }
)(Topbar);
