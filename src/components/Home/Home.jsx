import React, { Component } from "react";
import NewPost from "../NewPost/NewPost";
import Feed from "../Feed/Feed";
import Sidebar from "../Sidebar/Sidebar";
import Topbar from "../Topbar/Topbar";

import "./Home.css";

class Home extends Component {
  state = {};

  render = () => {
    return (
      <>
        <Topbar title="News Feed" />
        <Sidebar />
        <div className="main">
          <NewPost />
          <Feed />
        </div>
      </>
    );
  };
}

export default Home;
