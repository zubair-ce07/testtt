import React, { Component } from "react";
import { connect } from "react-redux";

import { logout } from "../../actions/user.action";

import "./Topbar.css";

class Topbar extends Component {
  state = {};

  render = () => {
    return (
      <div className="Topbar">
        <div className="title">News Feed</div>
        <button className="btn btn-light" onClick={this.props.logout}>
          Log out
        </button>
      </div>
    );
  };
}

export default connect(
  null,
  { logout }
)(Topbar);
