import React, { Component } from "react";
import { Route } from "react-router-dom";
import "./App.css";
import Employee from "./employee/Employee";
import Hierarchy from "./hierarchy/Hierarchy";
import { loggedIn } from "../auth.js";

class App extends Component {
  componentDidMount() {
    this.props.getProfile(localStorage.username);
  }

  render() {
    return (
      <div className="App">
        {loggedIn() && <Employee emp={this.props.profile} />}
        <br />
        {/* <Hierarchy tree={this.state.hierarchy} /> */}
      </div>
    );
  }
}

export default App;
