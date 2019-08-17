import React, { Component } from "react";
import FriendFinder from "../FriendFinder/FriendFinder";

import "./Sidebar.css";

class Sidebar extends Component {
  state = {};

  render = () => {
    return (
      <div className="Sidebar">
        <FriendFinder />
      </div>
    );
  };
}

export default Sidebar;
