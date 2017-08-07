import React, { Component } from "react";
import { Route } from "react-router-dom";
import "./App.css";
import Employee from "./employee/Employee";
import Hierarchy from "./hierarchy/Hierarchy";
import { loggedIn } from "../auth.js";
import djangoapi from "../djangoapi";

class App extends Component {
  constructor(props) {
    super();
    this.state = {
      profile: {},
      hierarchy: {
        name: "Top Level",
        children: [
          {
            name: "Level 2: A",
            children: [{ name: "Son of A" }, { name: "Daughter of A" }]
          },
          { name: "Level 2: B" }
        ]
      }
    };
  }

  componentDidMount() {
    djangoapi.getProfile(jsonData => {
      this.setState({
        profile: jsonData
      });
    });
  }

  render() {
    return (
      <div className="App">
        {loggedIn() && <Employee emp={this.state.profile} />}
        <br />
        <Hierarchy tree={this.state.hierarchy} />
      </div>
    );
  }
}

export default App;
