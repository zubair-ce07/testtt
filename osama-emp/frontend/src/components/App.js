import React, { Component } from "react";
import { Route } from "react-router-dom";
import "./App.css";
import Employee from "./Employee";
import { loggedIn } from "../auth.js";
import djangoapi from "../djangoapi";

class App extends Component {
  constructor(props) {
    super();
    this.state = {
      profile: {},
      hierarchy: {}
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
        {loggedIn() &&
          <Employee emp={this.state.profile} />}
      </div>
    );
  }
}

export default App;
